import pandas as pd


class CsvReader:
    def __init__(self):
        self.delimiter = ';'
        self.encoding = 'UTF-8'

    def get_delimiter(self):
        return self.delimiter

    def set_delimiter(self, value):
        self.delimiter = value

    def read(self, delimiter: str, file_path: str) -> pd.DataFrame:
        with open(file_path, 'r', encoding=self.encoding) as file:
            res = pd.read_csv(file, delimiter=delimiter)
        return res

