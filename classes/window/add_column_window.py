import tkinter as tk


class AddColumnWindow(tk.Toplevel):
    def __init__(self, parent: tk.Tk, external_fn):
        super().__init__(parent)
        self.label = tk.Label(self, text="Enter new column name:")
        self.entry = tk.Entry(self)
        self.ext_add_function = external_fn
        self.btn_add = tk.Button(self, text="Add new column", command=self.local_add_function)
        self.init_widgets()

    def init_widgets(self):
        self.label.grid(row=0, column=0, sticky='w')
        self.entry.grid(row=0, column=1, sticky='e')
        self.btn_add.grid(row=1, column=0, sticky='nswe')
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def local_add_function(self):
        new_val = self.entry.get()
        self.ext_add_function(new_val)
