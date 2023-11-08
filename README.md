﻿# 사용 세팅
먼저 discord에 message intent를 포함한 기능들을 체크한 봇을 2OATH의 url 생성에서 bot체크, administer체크하여 url 복사
이후 링크로 접속하여 봇을 추가할 서버를 선택한다. 그리고 설정에 가서 개발자 모드를 켠 다음에 봇이 채팅을 보낼 

## 토큰을 저장하는 방법
ChatGPT와 디스코드 봇의 보안을 유지하는 일은 중요합니다.
이 파일이 있는 경로에 '.env'를 추가하고, 아래와 같이 입력합니다
> OPENAI_API_KEY=[ChatGPT 키]
> DISCORD_TOKEN=[디스코드 봇 키]
그리고 os.getenv("OPENAI_API_KEY")와 같은 형식으로 코드에서 읽어들일 수 있습니다.

필요한 데이터 목록
- OPEN_API_KEY
- DISCORD_TOKEN