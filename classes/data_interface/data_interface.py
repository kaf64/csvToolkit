import numpy as np
import pandas as pd


class DataInterface:
    def __init__(self):
        self.data = None

    def init_data(self, data_to_init):
        self.data = data_to_init

    def add_column(self, new_column_name: str) -> None:
        column_list = self.data.columns.to_list()
        if new_column_name not in column_list and len(new_column_name) > 0 and new_column_name != ' ':
            new_series = pd.Series([])
            self.data.insert(loc=len(column_list), column=new_column_name, value=new_series)

    def remove_column(self, delete_column_name):
        if delete_column_name in self.data.columns:
            self.data.drop(columns=delete_column_name, inplace=True)

    def add_new_item(self, new_values: dict) -> None:
        new_item = pd.Series(data=new_values.values(), index=self.data.columns)
        self.data.loc[len(self.data)] = new_item

    def update_item(self, index, new_values):
        self.data.iloc[int(index), :] = pd.Series(new_values.values())

    def delete_item(self, index):
        if index in self.data.index:
            self.data.drop(inplace=True, index=index)

    def find_value(self, value):
        mask = np.column_stack([self.data[col].astype(str).str.contains(value, case=False, na=False)
                                for col in self.data])
        res = self.data.loc[mask.any(axis=1)]
        return res

