import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np


class ProcessFrame(tk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.data = None
        # init widgets
        frame_delete_nan = tk.LabelFrame(self, text='Delete empty values')
        frame_delete_nan.grid(row=0, column=0, sticky='nswe')
        frame_fill_nan = tk.LabelFrame(self, text='Fill empty values')
        frame_fill_nan.grid(row=1, column=0, sticky='nswe')
        frame_new_column = tk.LabelFrame(self, text='Add new column')
        frame_new_column.grid(row=3, column=0, sticky='NSWE')
        frame_delete_column = tk.LabelFrame(self, text='Delete column')
        frame_delete_column.grid(row=4, column=0, sticky='NSWE')
        # widgets for delete empty values
        self.label_list = tk.Label(frame_fill_nan, text='Select column :')
        self.label_list.grid(row=0, column=0)

        self.btn_delete_nan = tk.Button(frame_delete_nan,
                                        command=lambda: self.delete_nan(column=str(self.list_columns.get())),
                                        text='Delete rows with empty values')
        self.btn_delete_nan.grid(row=0, column=0)
        # widgets for fill empty values
        self.label_replace_column = tk.Label(frame_fill_nan, text='Select column')
        self.label_replace_column.grid(row=0, column=0)
        self.list_columns = ttk.Combobox(frame_fill_nan)
        self.list_columns.grid(row=0, column=1)
        self.label_replace = tk.Label(frame_fill_nan, text='Select value to replace empty values')
        self.label_replace.grid(row=1, column=0)
        self.entry_replace = tk.Entry(frame_fill_nan)
        self.entry_replace.grid(row=1, column=1)
        self.btn_replace_nan = tk.Button(frame_fill_nan,
                                        command=lambda: self.replace_nan(
                                            column=str(self.list_columns.get()),
                                            new_value=self.entry_replace.get()),
                                        text='Replace empty values')
        self.btn_replace_nan.grid(row=2, column=0)
        #widgets for adding new column
        self.label_add_col = tk.Label(frame_new_column, text='New column name:')
        self.label_add_col.grid(row=0, column=0)
        self.entry_add_col = tk.Entry(frame_new_column)
        self.entry_add_col.grid(row=0, column=1)
        label_init_val = tk.Label(frame_new_column, text='(optional) init value in new column:')
        label_init_val.grid(row=1, column=0)
        self.entry_init_val = tk.Entry(frame_new_column)
        self.entry_init_val.grid(row=1, column=1)
        self.btn_add_col = tk.Button(frame_new_column,
                                         command=lambda: self.add_new_column(column_name=str(self.entry_add_col.get()),
                                                                             init_value=str(self.entry_init_val.get())),
                                         text='add new column')
        self.btn_add_col.grid(row=2, column=0)
        # add widgets to delete column
        label_del_col = tk.Label(frame_delete_column, text='Set column to delete:')
        label_del_col.grid(row=0, column=0)
        self.list_del_col = ttk.Combobox(frame_delete_column)
        self.list_del_col.grid(row=0, column=1)
        btn_del_col = tk.Button(frame_delete_column,
                                text='Delete column',
                                command=lambda: self.delete_column(column_name=self.list_del_col.get()))
        btn_del_col.grid(row=1, column=0)

    def init_data(self, data: pd.DataFrame) -> None:
        self.data = data
        self.refresh_widgets()

    def refresh_widgets(self):
        list_container = self.data.columns.values.tolist()
        self.list_del_col['values'] = list_container
        list_container.append('all columns')
        self.list_columns['values'] = list_container

    def delete_nan(self, column: str) -> None:
        self.data.dropna(inplace=True)
        self.refresh_widgets()

    def replace_nan(self, column: str, new_value: str) -> None:
        if column.strip() is not None:
            if column == 'all columns':
                self.data.fillna(value=new_value, inplace=True)
            else:
                self.data[column].fillna(value=new_value, inplace=True)
            self.refresh_widgets()

    def add_new_column(self, column_name: str, init_value: str) -> None:
        if column_name.strip() is not None:
            self.data.insert(loc=len(self.data.columns), column=column_name, value=init_value)
        self.refresh_widgets()

    def delete_column(self, column_name: str) -> None:
        if column_name.strip() is not None:
            del self.data[column_name]
        self.refresh_widgets()
