# openNAMUbot
openNAMUbot는 Python을 사용해 openNAMU를 사용하는 위키의 봇을 작성하는 것을 돕는 라이브러리입니다  
**경고! 봇 사용을 허용하지 않는 위키에서 사용하지 마세요**
## 설치
openNAMUbot을 사용하기 위해서는 먼저 requests, bs4, reqeusts_toolbelt를 설치해야 합니다
```
pip install requests
pip intall beautifulsoup4
pip install reqeusts_toolbelt
```
openNAMUbot을 사용하는 파일과 같은 폴더 또는 Python 라이브러리 경로에 넣으면
```
import openNAMUbot
```
위 명령으로 openNAMUbot 라이브러리를 불러올 수 있습니다
## 사용법
openNAMUbot을 사용하기 위해서는 먼저 Session 객체를 만들어야 합니다
```
openNAMUbot.Session("https://2du.pythonanywhere.com")
```
https://2du.pythonanywhere.com 부분에는 사용할 openNAMU 위키의 주소를 넣으면 됩니다  
참고 : 밑의 예시에서는 Session 객체의 이름을 s로 지정했다고 가정합니다, (API)는 openNAMU에서 공식적으로 제공하는 API를 이용한 기능임을 표시합니다
### 로그인
```
s.login("1234", "5678")
```
1번째 인수는 ID, 2번째 인수는 비밀번호입니다  
**주의 : 계정에 2차 인증을 설정하지 마세요**  
로그인 없이도 사용이 가능하나, 권한이 필요한 작업(예 : 로그인 전용 문서 편집, 사용자 차단 등)은 로그인이 필요합니다
### 문서 읽기(API)
```
s.read("123", 4)
```
1번째 인수는 문서명, 2번째 인수는 리버전(생략 가능, 생략시 최신 리버전을 가져옴)입니다  
문서가 없거나 읽기 권한이 없을 경우 오류가 발생합니다  
### 문서 편집
```
s.edit("123", "456", "789", False)
```
1번째 인수 : 문서명
2번째 인수 : 문서 내용
3번째 인수(선택) : 편집 요약 (기본값은 편집 요악 없음)
4번째 인수(선택) : True일 경우 편집한 내용과 현재의 문서 내용이 같아도 편집, False일 경우 내용이 같으면 편집 안함 (기본값은 False)
### 랜덤 문서(API)
```
s.random_doc()
```
위키에 있는 모든 문서 중 아무거나 뽑아서 문서명을 불러옵니다
### 모든 문서
```
s.alldoc(0.1)
```
1번째 인수(선택) : 페이지 불러오기 딜레이 (초 단위, 기본값 0.1)  
위키에 있는 모든 문서를 AllDocIter 반복자로 반환합니다  
**참고로, 완전하진 않습니다(동일 문서가 2번 나오가나, 문서가 빠질 수 있음)**
### 사용자 차단
**이 기능은 사용자 차단 권한이 있는 계정으로 로그인해야 사용 가능합니다**
```
s.ban("123", "date", 1, "test", "normal", "")
```
1번째 인수 : 차단 대상 ID/IP  
2번째 인수 : 차단 기간 지정 방식  
* date : 날짜 지성
* days : 일수 지정

3번째 인수 : 일수(정수(1) 또는 문자열("1")) 또는 날짜 ("2024-12-05" 형식 문자열), 무기한 차단 시 2번째 인수는 date로, 3번째 인수는 빈 문자열로 하세요  
4번째 인수(선택) : 차단 사유 (생략시 없음)  
5번째 인수(선택) : 차단 종류 (기본값 normal)  
* normal : 일반
* regex : 정규표현식
* cidr : CIDR
* private : 비공개

6번째 인수(선택) : 차단 옵션 (기본값 "" (빈 문자열))  
* "" (빈 문자열) : 기본값
* login_able : 로그인 허용
* login_able_and_regsiter_disable : 로그인 허용 및 회원가입 비허용
* edit_request_able : 편집 요청 가능
* completely_ban : 완전 차단
* dont_come_this_site : 사이트 접근 차단
* release : 차단 해제 (차단 해제 시 2,3번째 인수는 무시됨)

### 이미지 업로드 (미구현)
```
s.upload("123", b"456", "direct_input", "")
```
1번째 인수 : 파일명  
2번째 인수 : 파일 내용 (bytes 포맷)  
3번째 인수(선택) : 라이선스 (기본값 direct_input)  
4번쨰 인수(선택) : 파일 문서의 본문 (기본값 "" (빈 문자열))  
## 예시
```
import openNAMUbot
s = openNAMUbot.Session("https://2du.pythonanywhere.com")
while True:
    d = s.random_doc()
    s.edit(d, s.read(d).replace('됬','됐'), '맞춤법 수정')
    print(d)
```
위 코드는 https://2du.pythonanywhere.com 위키의 문서의 '됬'을 '됐'으로 일괄 치환하되, "맞춤법 수정" 코멘트를 남깁니다