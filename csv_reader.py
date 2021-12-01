import csv


class CsvReader:
    def __init__(self):
        self.delimiter = ';'
        self.encoding = 'UTF-8'

    def get_delimiter(self):
        return self.delimiter

    def set_delimiter(self, value):
        self.delimiter = value

    def read(self, delimiter: str, file_path: str) -> dict:
        res = dict()
        data = list()
        # init index dictionary
        with open(file_path, 'r', encoding=self.encoding) as file:
            csv_reader = csv.DictReader(file, delimiter=delimiter)
            for line in csv_reader:
                data.append(line)
            res['data'] = data
            res['keys'] = csv_reader.fieldnames
            return res

