import tkinter as tk
from classes.window.field_window import FieldWindow


class EditWindow(FieldWindow):
    def __init__(self, parent: tk.Tk, content: dict, iid, data_interface) -> None:
        # function to save changes
        super().__init__(parent, content=content)
        self.data_interface = data_interface
        self.iid = iid
        self.title('Show/edit item')
        self.btn_save = tk.Button(self.btn_frame, text='Save changes', command=self.local_save_function)
        self.btn_reset = tk.Button(self.btn_frame, text='Reset unsaved changes', command=self.reset_changes)
        self.is_content_changed = False
        super().generate_field_in_frame()
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

    def get_iid(self) -> str:
        return self.iid

    def local_save_function(self):
        new_val = self.get_values()
        self.data_interface.update_item(index=self.iid, new_values=new_val)
        self.event_generate('<<DataUpdate>>')
        print("event_generated")
        self.is_content_changed = False

    def value_changed(self, *args):
        if self.is_content_changed is False:
            self.is_content_changed = True

    def get_is_content_changed(self):
        return self.is_content_changed

    def reset_changes(self):
        if self.is_content_changed is True:
            for key, value in self.content.items():
                self.local_values[key].set(value)
