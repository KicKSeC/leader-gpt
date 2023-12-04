import logging 
from settings import Settings
from openai import OpenAI


class ChatGPT:
    """ChatGPT의 API를 사용해 팀장으로서 답변을 생성"""
    gpt_model = {"gpt3.5": "gpt-3.5-turbo", "gpt4-turbo": "gpt-4-1106-preview"}
    # 팀장으로 설정하는 프롬프트
    system_role_prompt = "You are a supportive team leader and enabler of your teammates' goals."
    is_answering = False
    token_usage = 0  # 사용된 총 토큰 수
    __client = OpenAI(api_key=Settings.load('OPENAI_API_KEY'))

    class AlreadyAnsweringError(Exception):
        """ChatGPT는 한번에 하나만 답변 가능하므로 이미 답변 중일 때 발생하는 에러"""

        def __init__(self):
            message = "ChatGPT가 이미 답변 중입니다."
            logging.error(message)
            super().__init__(message)

    @staticmethod
    def get_response_object(message: str, model=gpt_model["gpt3.5"], user='user'):
        """챗지피티의 응답 객체 반환"""
        if ChatGPT.is_answering:
            raise ChatGPT.AlreadyAnsweringError()

        ChatGPT.is_answering = True
        logging.info('chatGpt answering')
        try:
            response = ChatGPT.__client.chat.completions.create(
                model=model,
                messages=[
                    {"role":"system", "content": ChatGPT.system_role_prompt},
                    {"role": user, "content": message}  # type: ignore
                ]  
            )
        finally:
            ChatGPT.is_answering = False

        if response.usage:
            ChatGPT.token_usage += response.usage.total_tokens
        return response

    # 응답 객체의 메세지 내용
    @staticmethod
    def get_response(message: str, model=gpt_model["gpt3.5"], user='user') -> str:
        """답변을 문자열로 반환"""
        result = ChatGPT.get_response_object(message, model=model, user=user).choices[0].message.content

        if not result:
            return "답변에 오류가 있었습니다."
        return result

    @staticmethod
    def get_response_by_stream(message: str, model=gpt_model["gpt3.5"], user='user'):
        '''답변을 streaming하게 받음'''
        try:
            if ChatGPT.is_answering:
                raise ChatGPT.AlreadyAnsweringError()

            ChatGPT.is_answering = True
            stream = ChatGPT.__client.chat.completions.create(
                model=model,
                messages=[
                        {"role":"system", "content": ChatGPT.system_role_prompt},
                        {"role":user, "content": message}   # type: ignore
                ], 
                stream=True
            )
            for chunk in stream:    # type: ignore
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        finally:
            ChatGPT.is_answering = False
        
        # stream의 경우 토큰을 셀 수 없다고 한다. 
            

    @staticmethod
    def get_token_usage():
        """지금까지 사용된 토큰 수"""
        return ChatGPT.token_usage

    # TODO 이어서 대화하기, 대화 끊기, 여러 개 동시에 대화하기


if __name__ == '__main__':
    INTRO = "3줄로 자기소개 부탁해"
    print(INTRO)
    print(ChatGPT.get_response(INTRO))
