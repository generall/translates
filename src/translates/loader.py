import random
from random import sample, choice

import pandas as pd
import glob
import os

from translates import DATA_PATH


class TextsLoader:

    def __init__(self, files):
        self.files = files

    def load_random(self):
        sample_file = choice(self.files)
        df = pd.read_csv(sample_file)

        sample_row = df.sample(1)

        return sample_row['en'].iloc[0], sample_row['ru'].iloc[0]


if __name__ == '__main__':

    path = os.path.join(DATA_PATH, "stories", "*")
    loader = TextsLoader(glob.glob(path))
    en, ru = loader.load_random()
    print(en)
    print(ru)
