from bs4 import BeautifulSoup as bs
from requests import get, post, session
from json import loads
from time import sleep
class Error(Exception):
    pass
class Session:
    def __init__(self, url):
        self.session = session()
        self.url = url.strip()
        if self.url[-1] == '/':
            self.url = self.url[:-1]
    def get(self, url):
        return self.session.get(self.url + '/' + url)
    def post(self, url, data, files = None):
        return self.session.post(self.url + '/' + url, data = data, files = files)
    def login(self, id, pw):
        r = self.post('login', {"id" : id, "pw" : pw})
        if r.status_code != 200:
            raise Error(bs(r.text, 'lxml').select_one("#main_data > div > ul > li").text)
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
    def edit(self, doc, data, send = '', ignoreEqual = False):
        b = bs(self.get('edit/' + doc).text, 'lxml')
        v = b.select_one("input[name='ver']")['value']
        if ignoreEqual or b.select_one("#opennamu_edit_textarea").text != data:
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
    def ban(self, id, dt, dr, res = "", type = "normal", option = ""):
        rq = {
            'name' : id,
            'date_type' : dt,
            'date_days' : dr,
            'date' : dr,
            'why' : res,
            'do_ban_type' : type,
            'ban_option' : option
        }
        r = self.post('auth/ban', rq)
        if r.status_code == 400:
            raise Error("권한이 없습니다")
    def upload(self, name, content, license = 'direct_input', content2 = ""):
        raise NotImplementedError("해당 기능은 개발 중입니다")
    def alldoc(self, delay = 0.1):
        return AllDocIter(self.session, delay)
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
