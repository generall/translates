import re
from pprint import pprint

import nltk
from translates import DATA_PATH


nltk.data.path.append(DATA_PATH)


class TextAligner:
    """
    This class should aling 2 texts into parallel sentences.

    """
    def __init__(self):
        pass

    def split_sentences(self, text, lang=None):

            text = re.sub('\([^\)]+\)', '', text)
            text = re.sub('e.g.', 'For example', text, flags=re.IGNORECASE)  # Because fuck abbreviations
            return nltk.sent_tokenize(text, lang)

    def align(self, text_en, text_ru):
        return zip(
            self.split_sentences(text_en, 'english'),
            self.split_sentences(text_ru, 'russian'),
        )


if __name__ == '__main__':

    aligner = TextAligner()

    text_ru = "Music has become the main activity because you don’t need much time to listen to music or you can do " \
              "it with other things. (e.g. make your homework or cooking) Many young people regularly go out on " \
              "Friday or Saturday nights to a disco or to a concert. "
    text_en = "Музыка стала популярным занятием, потому что для прослушивания музыки не нужно много времени, " \
              "или вы можете слушать ее, одновременно занимаясь другими делами. (например, делать уроки или готовить) " \
              "Многие молодые люди регулярно ходят по пятницам или субботам на дискотеку или концерт. "

    for match in aligner.align(text_en, text_ru):
        print(match)
