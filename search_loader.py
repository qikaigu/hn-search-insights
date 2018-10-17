import os.path
import json
from json import JSONDecodeError
import zipfile
import pandas as pd


class SearchLoader:

    def __init__(self, config):
        self.input_file = config['input']
        if not os.path.isfile(self.input_file):
            raise Exception("Input file doesn't exist.")

    def load(self):
        data = []
        with zipfile.ZipFile(self.input_file) as zfile:
            for finfo in zfile.infolist():
                with zfile.open(finfo) as ifile:
                    data.extend(ifile.readlines())

        valid_searches = []
        for d in data:
            try:
                search = json.loads(d)
                valid_searches.append(search)
            except JSONDecodeError:
                pass

        df = pd.DataFrame(valid_searches)
        return df
