# 실패작. 봇 체크에서 걸림 
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from bs4 import BeautifulSoup
import time

url = 'https://chat.openai.com/?model=text-davinci-002-render-sha'
prompt_xpath = '//*[@id="prompt-textarea"]'
prompt_send_xpath = '//*[@id="__next"]/div[1]/div[2]/main/div[1]/div[2]/form/div/div[2]/div/button'
response_xpath = '//*[@id="__next"]/div[1]/div[3]/main/div[1]/div[1]/div/div/div/div[last()]/div/div/div[2]/div/div[1]/div/div'

driver = Driver(browser="chrome", headless=False, disable_gpu=True)
driver.get(url)
driver.implicitly_wait(1)
# //*[@id="__main"]/main/div/div[2]/div/div/div/div[2]/div/div[3]/textarea

def get_response(message):
    global driver
    promptta = driver.find_element(By.XPATH, prompt_xpath)
    promptta.send_keys(message)
    driver.find_element(By.XPATH, prompt_send_xpath).click()
    time.sleep(5)
    
    response_div = driver.find_element(By.XPATH, response_xpath)
    soup = BeautifulSoup(response_div, 'html.parser')
    
    elements = []
    for element in soup.find_all(['p', 'ol', 'ul']):
        if element.name == 'p':
            elements.append(element.text)
        else:
            for li in element.find_all('li'):
                elements.append(li.text)
    return '\n'.join(elements)

if __name__ == '__main__':
    message = "자기소개와 자신이 뭘 할 수 있는지 알려줘"
    response = get_response(message)
    print(response)
    
driver.close()