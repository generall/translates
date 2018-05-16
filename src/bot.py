"""
Telegram bot for translation exercise
"""
import glob
import logging
import os
import sys

from collections import defaultdict

import simplediff
import nltk

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from translates import DATA_PATH
from translates.loader import TextsLoader


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


class SentenceDialog:
    def __init__(self):
        self.dialogs = defaultdict(dict)
        path = os.path.join(DATA_PATH, "stories", "*")
        self.loader = TextsLoader(glob.glob(path))

    def get_new_text(self):
        en, ru = self.loader.load_random()
        return {
            'en_text': en,
            'ru_text_orig': ru,
            "ru_text_translate": ''
        }

    def red(self, text):
        result = ''
        for c in text:
            result = result + c + '\u0336'
        return result

    def show_diff(self, orig, user):
        diff = simplediff.diff(nltk.word_tokenize(orig), nltk.word_tokenize(user))
        html = ""
        for op, part in diff:
            part_text = ' '.join(part)
            if op == '=':
                html += part_text
            if op == '+':
                html += self.red(part_text)
            if op == '-':
                html += ' .. ' * len(part)

        return html

    def handle_message(self, bot, update):
        telegram_chat = str(update.message.chat_id)
        telegram_user = update.message.from_user.username or ''

        cmd = update.message.text.split()

        if cmd[0] == "/start":
            self.dialogs[(telegram_chat, telegram_user)] = {}

        dailog_data = self.dialogs[(telegram_chat, telegram_user)]
        state = dailog_data.get('state')

        if state is None:
            texts = self.get_new_text()

            bot.send_message(
                chat_id=update.message.chat_id,
                parse_mode="Markdown",
                text="Orig: {}".format(texts['ru_text_orig'])
            )

            self.dialogs[(telegram_chat, telegram_user)] = {
                'state': 'asked',
                **texts
            }
        elif state == 'asked':

            inp_text = update.message.text

            if inp_text == state:
                texts = self.get_new_text()
                bot.send_message(
                    chat_id=update.message.chat_id,
                    parse_mode="Markdown",
                    text="Orig: {}".format(texts['ru_text_orig'])
                )

                self.dialogs[(telegram_chat, telegram_user)] = {
                    'state': 'asked',
                    **texts
                }
            else:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    parse_mode="Markdown",
                    text="Diff: {}".format(self.show_diff(dailog_data.get('en_text'), inp_text))
                )


if __name__ == '__main__':

    token = os.environ.get('TELEGRAM_TOKEN')

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    setup_logging(logging.INFO)

    dialogs = SentenceDialog()

    message_handler = MessageHandler(Filters.text, dialogs.handle_message)
    dispatcher.add_handler(message_handler)

    updater.start_polling()

