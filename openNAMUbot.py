from bs4 import BeautifulSoup as bs
from requests import get, post, session
from json import loads
from time import sleep
class LoginFailError(Exception):
    pass
class Error(Exception):
    pass
class Session:
    def __init__(self, url):
        self.session = session()
        self.url = url
    def get(self, url):
        return self.session.get(self.url + '/' + url)
    def post(self, url, data):
        return self.session.post(self.url + '/' + url, data)
    def login(self, id, pw):
        r = self.post('login', {"id" : id, "pw" : pw})
        if r.status_code != 200:
            raise LoginFailError(bs(r.text, 'lxml').select_one("#main_data > div > ul > li").text)
    def logout(self):
        self.get('logout')
    def read(self, doc, rev = None):
        if rev == None:
            r = loads(self.get('api/raw/' + doc).text)
        else:
            r = loads(self.get('api/raw_rev/{0}/{1}'.format(rev, doc)).text)
        if r == {}:
            raise Error("존재하지 않는 문서 또는 리버전입니다")
        elif r == {"response":"require auth"}:
            raise Error("읽기 권한이 부족합니다")
        else:
            return r["data"]
    def edit(self, doc, data, send = ''):
        v = bs(self.get('edit/' + doc).text, 'lxml').select_one("input[name='ver']")['value']
        self.post('edit/' + doc, {
            'doc_section_data_where' : '',
            'doc_section_edit_apply' : 'X',
            'ver' : v,
            'send' : send,
            'doc_data_org' : '',
            'document_markup' : 'namumark',
            'content' : data
            })
    def random_doc(self):
        return loads(self.get('api/random').text)["data"]
class AllDocIter:
    def __init__(self, session, delay = 0.1):
        self.session = session
        self.page = 0
        self.delay = delay
        self.cntPage = None
        self.cpInd = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.cntPage == None or self.cpInd >= len(self.cntPage):
            self.page += 1
            self.cntPage = [x.text for x in bs(self.session.get('list/document/all/' + str(self.page)).text, 'lxml').select("#main_data > div > ul > li > a")]
            sleep(self.delay)
            self.cpInd = 0
            if len(self.cntPage) == 0:
                raise StopIteration
        self.cpInd += 1
        return self.cntPage[self.cpInd - 1]
