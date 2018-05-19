import os
import requests


class Translator:

    def __init__(self):
        pass

    def translate(self, text: str, from_lang='en', to_lang='ru') -> str:
        raise NotImplemented()


class YandexTranslator(Translator):
    def __init__(self, api_key=None):
        super().__init__()

        self.api_key = api_key or os.environ.get("YANDEX_API_KEY")

        self.url = "https://translate.yandex.net/api/v1.5/tr.json/translate"

    def translate(self, text: str, from_lang='en', to_lang='ru'):
        if self.api_key:
            querystring = {
                "key": self.api_key,
                "text": text,
                "lang": "{}-{}".format(from_lang, to_lang)
            }

            response = requests.request("GET", self.url, params=querystring)

            resp = response.json()

            return resp['text'][0]
        else:
            return None


if __name__ == '__main__':
    translator = YandexTranslator()
    ru_text = translator.translate("However there are only a few controlled studies which confirm this finding.")
    print(ru_text)
