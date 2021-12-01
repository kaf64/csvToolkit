import csv


class CsvWriter:
    def __init__(self):
        self.delimiter = ';'
        self.encoding = 'UTF-8'

    def write(self, file_path: str, data: list, columns: list) -> None:
        with open(file_path, 'w', encoding=self.encoding, newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=columns, delimiter=self.delimiter)
            csv_writer.writeheader()
            for line in data:
                csv_writer.writerow(line)
