﻿import os       # 환경 변수 접근
import openai
from openai import OpenAI


class ChatGPT:
    '''ChatGPT의 API를 사용해 팀장으로서 답변을 생성'''
    gpt_model = {"davinci": "text-davinch-003", "gpt3.5": "gpt-3.5-turbo",
                "babbage": "babbage-002", "gpt4": "gpt-4", "gpt4-turbo": "gpt-4-1106-preview"}
    # 팀장으로 설정하는 프롬프트
    system_role = {"role": "system",
                "content": "You are a supportive team leader and enabler of your teammates' goals."}
    is_answering = False
    token_usage = 0     # 사용된 총 토큰 수
    __client = OpenAI()

    class AlreadyAnsweringError(Exception):
        """ChatGPT는 한번에 하나만 답변 가능하므로 이미 답변 중일 때 발생하는 에러"""
        def __init__(self):
            super().__init__("ChatGPT가 이미 답변 중입니다.") 
        
    @staticmethod
    def get_response_object(message, model=gpt_model["gpt3.5"], user='user'): 
        """챗지피티의 응답 객체 반환"""
        if ChatGPT.is_answering:
            raise ChatGPT.AlreadyAnsweringError()

        ChatGPT.is_answering = True
        response = ChatGPT.__client.chat.completions.create(
            model=model, messages=[ChatGPT.system_role, {"role": user, "content": message}]
        )
        ChatGPT.is_answering = False

        ChatGPT.token_usage += response.usage.total_tokens
        
        return response

    # 응답 객체의 메세지 내용
    @staticmethod
    def get_response(message, model=gpt_model["gpt3.5"], user='user'):
        """답변을 문자열로 반환"""
        try:
            return ChatGPT.get_response_object(message, model=model, user=user).choices[0].message.content
        except openai.BadRequestError:
            return '답변에 오류가 발생하였습니다.'
        # try: 
        #     return get_response_object(message, user=user).choice[0].message.content
        # except Exception as e:
        #     print(e)
        #     return "에러 발생!"

    @staticmethod
    def get_token_usage(): 
        """지금까지 사용된 토큰 수"""
        return ChatGPT.token_usage

    # TODO 이어서 대화하기, 대화 끊기, 여러 개 동시에 대화하기

if __name__ == '__main__':
    INTRO = "간략히 자기소개 부탁해"
    print(INTRO + ": " + ChatGPT.get_response(INTRO))
    