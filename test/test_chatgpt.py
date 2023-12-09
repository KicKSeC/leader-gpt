import logging
import os
import sys
from chatgpt import ChatGPT 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


logging.basicConfig(filename='test\\test.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

ans_txt = "답변: "
logging.info('start answer')
stream = ChatGPT.get_response_by_stream("Say 'this is a test'")

while True:
    try: 
        logging.info('answering...')
        txt = next(stream)
        print(txt) 
    except StopIteration:
        logging.info("end answer")
        break
    
print(ans_txt)
