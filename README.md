# 사용 세팅

## 토큰을 저장하는 방법
ChatGPT와 디스코드 봇의 보안을 유지하는 일은 중요합니다.
이 파일이 있는 경로에 '.env'를 추가하고, 아래와 같이 입력합니다
> OPENAI_API_KEY=[ChatGPT 키]
> DISCORD_TOKEN=[디스코드 봇 키]
그리고 os.getenv("OPENAI_API_KEY")와 같은 형식으로 코드에서 읽어들일 수 있습니다.

필요한 데이터 목록
- OPEN_API_KEY
- DISCORD_TOKEN