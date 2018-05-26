import glob
import json
import os
from collections import defaultdict

from flask import Flask, request, jsonify, send_from_directory

from translates import STATIC_PATH, DATA_PATH
from translates.loader import TextsLoader
from translates.translate import YandexTranslator

app = Flask(__name__, static_url_path=STATIC_PATH)


class Controller:
    def __init__(self):
        self.dialogs = defaultdict(dict)
        path = os.path.join(DATA_PATH, "stories", "yandex*")
        self.loader = TextsLoader(glob.glob(path))
        self.translator = YandexTranslator()
        self.filename = os.path.join(DATA_PATH, "saved.tsv")

    def get_new_text(self):
        en, ru = self.loader.load_random()
        return {
            'en_text': en,
            'ru_text_orig': ru,
            "ru_text_translate": self.translator.translate(en, from_lang='en', to_lang='ru')
        }

    def save_answer(self, data):
        with open(self.filename, 'a') as fd:
            fd.write("{}\t{}\n".format(data['en_text'], data['user_text']))


ctl = Controller()


@app.route("/get_next")
def get_next():
    return jsonify(ctl.get_new_text())


@app.route("/commit", methods=['POST'])
def commit():
    content = request.get_json(silent=True)
    ctl.save_answer(content)
    return get_next()


@app.route('/page/<path:path>')
def static_file(path):
    return send_from_directory(STATIC_PATH, path)

