# openNAMUbot
openNAMUbot는 Python을 사용해 openNAMU를 사용하는 위키의 봇을 작성하는 것을 돕는 라이브러리입니다<br>
**경고! bot 사용을 허용하지 않는 위키에서 사용하지 마세요**
## 설치
openNAMUbot을 사용하기 위해서는 먼저 requests, bs4를 설치해야 합니다
```
pip install requests
pip intall beautifulsoup4
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
(참고 : URL 뒤에 /를 넣지 마세요 (```https://2du.pythonanywhere.com/``` (X), ```https://2du.pythonanywhere.com``` (O))
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
s.edit("123", "456", "789")
```
1번째 인수는 문서명, 2번째 인수는 문서 내용, 3번째 인수는 편집 요약(생략 가능)입니다
### 랜덤 문서(API)
```
s.random_doc()
```
위키에 있는 모든 문서 중 아무거나 뽑아서 문서명을 불러옵니다
### 모든 문서
```
AllDocIter(s, 0.1)
```
모든 문서를 불러올 때는 AllDocIter 반복자를 사용하며, 1번째 인수는 Session 객체, 2번째 인수는 페이지를 불러오는 딜레이(초 단위, 기본값 0.1)입니다
**참고로, 완전하진 않습니다(동일 문서가 2번 나오가나, 문서가 빠질 수 있음)**