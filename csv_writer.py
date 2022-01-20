import pandas as pd


class CsvWriter:
    def __init__(self):
        self.delimiter = ';'
        self.encoding = 'UTF-8'

    def write(self, file_path: str, data: pd.DataFrame) -> None:
        data.to_csv(path_or_buf=file_path, sep=self.delimiter, index=False)
