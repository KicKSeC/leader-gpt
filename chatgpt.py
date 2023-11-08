import os
import openai
import logging

openai.api_key = os.getenv('OPENAI_API_KEY') 
logging.basicConfig(filename='chatgpt.log', filemode='w', level=logging.INFO ,
                    format='%(name)s - %(levelname)s - %(message)s')
gpt_model = {"davinci": "text-davinch-003", "gpt3.5": "gpt-3.5-turbo", 
             "babbage": "babbage-002", "gpt4": "gpt-4", "gpt4-turbo": "gpt-4-1106-preview"}
system_role = {"role": "system", 
               "content": "You are a supportive team leader and enabler of your teammates' goals."}

token_usage = 0     # 사용된 총 토큰 수 
def _increase_token_usage(tokens):
    global token_usage
    token_usage += tokens
    logging.info('token increased')
    
# 인공지능의 응답 객체 반환
def get_response_object(message, model=gpt_model["gpt3.5"], user='user'): 
    logging.info('await to get response')
    response = openai.ChatCompletion.create(
        model=model, messages=[system_role, {"role": user, "content": message}]
    )
    
    logging.info('getting token usage')
    _increase_token_usage(response.usage.total_tokens)
    
    return response

# 응답 객체의 메세지 내용
def get_response(message, model=gpt_model["gpt3.5"], user='user'):
    logging.info('returning message')
    try:
        return get_response_object(message, model=model, user=user).choices[0].message.content
    except openai.error.InvalidRequestError as e:
        logging.error(e)
        return '답변에 오류가 발생하였습니다.'
    # try: 
    #     return get_response_object(message, user=user).choice[0].message.content
    # except Exception as e:
    #     print(e)
    #     return "에러 발생!"

def get_token_usage(): 
    return token_usage

# TODO 이어서 대화하기, 대화 끊기, 여러 개 동시에 대화하기 

