import tkinter as tk


class AddColumnWindow(tk.Toplevel):
    def __init__(self, parent: tk.Tk, data_interface):
        super().__init__(parent)
        self.data_interface = data_interface
        self.label = tk.Label(self, text="Enter new column name:")
        self.entry = tk.Entry(self)
        self.btn_add = tk.Button(self, text="Add new column", command=self.local_add_column_function)
        self.init_widgets()

    def init_widgets(self):
        self.label.grid(row=0, column=0, sticky='w')
        self.entry.grid(row=0, column=1, sticky='e')
        self.btn_add.grid(row=1, column=0, sticky='nsew')
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def local_add_column_function(self):
        new_val = self.entry.get()
        self.data_interface.add_column(new_val)
        self.event_generate('<<DataUpdate>>')
