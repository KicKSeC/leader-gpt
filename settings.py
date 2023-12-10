import os
import json
import logging


class Settings:
    """사용자로부터 입력에 필요한 데이터를 입력받는 클래스"""
    path_setting = os.path.join("data", "settings.json")
    path_data = os.path.join("data", "data.json")

    @classmethod
    def initial_setting(cls):
        """실행 시 모자란 파일을 메꿈"""
        if not os.path.isdir('data'):
            os.mkdir('data')

        if not os.path.isfile(cls.path_setting):
            with open(cls.path_setting, "w", encoding='utf-8') as f:
                settings = {"channel": None, "members": []}
                json.dump(settings, f)
        if not os.path.isfile(cls.path_data):
            with open(cls.path_data, "w", encoding='utf-8') as f:
                data = {"assignment": {}, "schedule": []}
                json.dump(data, f)

        logging.basicConfig(filename='data/bot.log', level=logging.DEBUG,  # 로그 파일 설정
                            format='%(asctime)s:%(levelname)s:%(message)s')

        if Settings.load('OPENAI_API_KEY', is_setting=True) is None:
            print("OpenAI API key 값이 없습니다.\nOpenAI API key: ", end='')
            key = input()
            Settings.save('OPENAI_API_KEY', key, is_setting=True)
        if Settings.load('DISCORD_TOKEN', is_setting=True) is None:
            print("Discord 봇 토큰이 없습니다.\nEnter Discord token: ", end='')
            key = input()
            Settings.save('DISCORD_TOKEN', key, is_setting=True)

    @classmethod
    def save(cls, key, data, is_setting=False):
        """
        settings.json이나 data.json과 같은 json 파일에 접근하여 데이터를 저장오는 함수
        Args:
            is_setting: setting.json에 접근할 것인지 여부. 기본값 False라면 data에 접근한다.
        """
        path = cls.path_data if not is_setting else cls.path_setting
        
        if not os.path.isfile(path):
            raise FileNotFoundError('대상 파일을 찾을 수 없습니다')
        
        with open(path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        content[key] = data
        logging.info(data)
        with open(path, 'w', encoding='utf-8') as f:
            try: 
                json.dump(content, f, indent=4)
            except TypeError as e:
                logging.error("저장할 수 없는 값: %s", e)

    @classmethod
    def load(cls, key: str, is_setting=False):
        """
        settings.json이나 data.json과 같은 json 파일에 접근하여 데이터를 불러오는 함수
        Args:
            is_setting: setting.json에 접근할 것인지 여부. 기본값 False라면 data에 접근한다.
        """
        path = cls.path_data if not is_setting else cls.path_setting

        if not os.path.isfile(path):
            raise FileNotFoundError('대상 파일을 찾을 수 없습니다')

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f).get(key)

        return data

    @classmethod
    def delete(cls, key: str):
        """주어진 키의 값을 삭제. 성공하면 True, 실패하면 False"""
        with open(cls.path_setting, 'r', encoding='utf-8') as f:
            content = json.load(f)
        if content.get(key) is None:
            return False
        del content[key]
        with open(cls.path_setting, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=4)


Settings.initial_setting()
