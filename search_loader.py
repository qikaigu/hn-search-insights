import os.path
import json
from json import JSONDecodeError
import zipfile
import pandas as pd


class SearchLoader:

    def __init__(self, input_file=None):
        if input_file is None:
            self.input_file = 'input/hn_insights_data.zip'
        elif os.path.isfile(input_file):
            self.input_file = input_file
        else:
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
