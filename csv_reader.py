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
        # init index
        i = 0
        # init index dictionary
        index_dict = {
            'index': None
        }
        with open(file_path, 'r', encoding=self.encoding) as file:
            csv_reader = csv.DictReader(file, delimiter=delimiter)
            for line in csv_reader:
                # set correct number of index
                index_dict['index'] = str(i)
                # append index and readed line to data
                data.append(dict(**index_dict, **line))
                i += 1
            res['data'] = data
            res['keys'] = csv_reader.fieldnames
            return res

