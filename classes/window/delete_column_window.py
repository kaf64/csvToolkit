import tkinter as tk
from tkinter import ttk
from classes.window.field_window import FieldWindow


class DeleteColumnWindow(tk.Toplevel):
    def __init__(self, parent: tk.Tk, columns, data_interface):
        super().__init__(parent)
        self.parent = parent
        self.data_interface = data_interface
        self.frame = ttk.Frame(self)
        self.label = ttk.Label(self.frame, text="select column do delete:")
        self.columns = columns
        self.combobox = ttk.Combobox(self.frame)
        self.refresh_combobox()
        self.btn = tk.Button(self.frame, text="Delete column", command=lambda: self.delete_column())
        # organize widgets
        self.frame.grid(row=0, column=0)
        self.label.grid(row=0, column=0)
        self.combobox.grid(row=0, column=1)
        self.btn.grid(row=0, column=2)
        # configure columns
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        # configure rows
        self.rowconfigure(0, weight=1)

    def delete_column(self):
        col_str = str(self.combobox.get())
        self.data_interface.remove_column(delete_column_name=col_str)
        self.delete_column_local(col_str)
        self.refresh_combobox()
        self.event_generate('<<DataUpdate>>')

    def delete_column_local(self, col_str) -> None:
        if col_str in self.columns:
            self.columns.remove(col_str)

    def refresh_combobox(self) -> None:
        self.combobox['values'] = tuple(self.columns)
        if len(self.columns) > 0:
            self.combobox.set(self.columns[0])
        else:
            self.combobox.set("")

