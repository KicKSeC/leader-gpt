import os       # 환경 변수 접근
import openai


class ChatGPT:
    """챗지피티의 API를 활용한 클래스"""
    gpt_model = {"davinci": "text-davinch-003", "gpt3.5": "gpt-3.5-turbo", 
                "babbage": "babbage-002", "gpt4": "gpt-4", "gpt4-turbo": "gpt-4-1106-preview"}
    system_role = {"role": "system", 
                "content": "You are a supportive team leader and enabler of your teammates' goals."}
    openai.api_key = os.getenv('OPENAI_API_KEY') 
    is_answering = False

    class AlreadyAnsweringException(Exception):
        """ChatGPT는 한번에 하나만 답변 가능하므로 이미 답변 중일 때 발생하는 에러"""
        def __init__(self):
            super().__init__("ChatGPT가 이미 답변 중입니다.")

    def __init__(self) -> None:
        self.token_usage = 0     # 사용된 총 토큰 수 

    def _increase_token_usage(self, tokens):
        self.token_usage += tokens
        
    def get_response_object(self, message, model=gpt_model["gpt3.5"], user='user'): 
        """챗지피티의 응답 객체 반환"""
        if ChatGPT.is_answering:
            raise ChatGPT.AlreadyAnsweringException()
        ChatGPT.is_answering = True
        response = openai.ChatCompletion.create(
            model=model, messages=[self.system_role, {"role": user, "content": message}]
        )
        ChatGPT.is_answering = False

        self._increase_token_usage(response.usage.total_tokens)
        
        return response

    # 응답 객체의 메세지 내용
    def get_response(self, message, model=gpt_model["gpt3.5"], user='user'):
        """답변을 문자열로 반환"""
        try:
            return self.get_response_object(message, model=model, user=user).choices[0].message.content
        except openai.error.InvalidRequestError:
            return '답변에 오류가 발생하였습니다.'
        # try: 
        #     return get_response_object(message, user=user).choice[0].message.content
        # except Exception as e:
        #     print(e)
        #     return "에러 발생!"

    def get_token_usage(self): 
        """지금까지 사용된 토큰 수"""
        return self.token_usage

    # TODO 이어서 대화하기, 대화 끊기, 여러 개 동시에 대화하기 

