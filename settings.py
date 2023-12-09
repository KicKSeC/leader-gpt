import os
import json
import logging


class Settings:
    """사용자로부터 입력에 필요한 데이터를 입력받는 클래스"""
    path = os.path.join("data", "settings.json")

    @classmethod
    def initial_setting(cls):
        """실행 시 모자란 파일을 메꿈"""
        if not os.path.isdir('data'):
            os.mkdir('data')

        if not os.path.isfile(cls.path):
            with open(cls.path, "w", encoding='utf-8') as f:
                settings = {"channel": None, "members": []}
                json.dump(settings, f)

        logging.basicConfig(filename='data/bot.log', level=logging.DEBUG,  # 로그 파일 설정
                            format='%(asctime)s:%(levelname)s:%(message)s')

        if Settings.load('OPENAI_API_KEY') is None:
            print("OpenAI API key 값이 없습니다.\nOpenAI API key: ", end='')
            key = input()
            Settings.save('OPENAI_API_KEY', key)
        if Settings.load('DISCORD_TOKEN') is None:
            print("Discord 봇 토큰이 없습니다.\nEnter Discord token: ", end='')
            key = input()
            Settings.save('DISCORD_TOKEN', key)

    @classmethod
    def save(cls, key, data):
        """setting.json으로부터 채널 정보를 저장함"""

        with open(cls.path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        content[key] = data
        with open(cls.path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=4)

    @classmethod
    def load(cls, key: str):
        """setting.json으로부터 채널 정보를 불러옴"""
        with open(cls.path, 'r', encoding='utf-8') as f:
            data = json.load(f).get(key)

        return data

    @classmethod
    def delete(cls, key: str):
        """주어진 키의 값을 삭제. 성공하면 True, 실패하면 False"""
        with open(cls.path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        if content.get(key) is None:
            return False
        del content[key]
        with open(cls.path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=4)


Settings.initial_setting()
