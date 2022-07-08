import tkinter as tk
from tkinter import ttk, messagebox
from classes.window.field_window import FieldWindow


class AddWindow(FieldWindow):
    def __init__(self, parent: tk.Tk, external_fn, content: dict) -> None:
        # function to save changes
        self.ext_function = external_fn
        super().__init__(parent, content=content)
        #self.content = dict()
        self.content = content
        self.title('Add new item')
        self.btn_save = tk.Button(self.btn_frame, text='Add new item', command=self.local_add_function)
        self.btn_reset = tk.Button(self.btn_frame, text='Clear values', command=self.clear_fields)
        self.is_content_changed = False
        super().generate_field_in_frame(content)
        self.organize_widgets()
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def organize_widgets(self) -> None:
        super().organize_widgets()
        self.btn_save.grid(row=0, column=0, padx=10, sticky='nw')
        self.btn_reset.grid(row=0, column=1, sticky='nw')

    def get_values(self) -> dict:
        # get vars from strvars
        res = dict()
        for key, val in self.local_values.items():
            res[key] = val.get()
        return res
        dict_val = None
        dict_key = None
        for dictionary in self.local_values:
            for key, value in dictionary.items():
                if key == 'column_name':
                    dict_key = value
                elif key == 'value':
                    dict_val = value.get()
                if dict_key and dict_val:
                    res[dict_key] = dict_val
                    dict_val = None
                    dict_key = None
        return res

    def clear_fields(self):
        for key, val in self.local_values.items():
            val.set("")

    def local_add_function(self):
        new_val = self.get_values()
        self.ext_function(new_val)
        self.clear_fields()
        self.is_content_changed = False

    def value_changed(self, *args):
        if self.is_content_changed is False:
            self.is_content_changed = True

    def get_is_content_changed(self):
        return self.is_content_changed


