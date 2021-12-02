import tkinter as tk
from tkinter import ttk, messagebox


class EditWindow(tk.Toplevel):
    def __init__(self, parent: tk.Tk, content: dict, iid, external_fn) -> None:
        super().__init__(parent)
        self.content = content
        self.iid = iid
        self.title('Show/edit item')
        # init list of local values StringVars type
        self.local_values = dict()
        self.ext_save_function = external_fn
        self.main_canvas = tk.Canvas(self, borderwidth=0)
        self.main_frame = tk.Frame(self.main_canvas)
        self.btn_frame = tk.Frame(self.main_frame)
        self.btn_save = tk.Button(self.btn_frame, text='Save changes', command=self.local_save_function)
        self.btn_reset = tk.Button(self.btn_frame, text='Reset unsaved changes', command=self.reset_changes)
        self.is_content_changed = False
        # add scrollbar
        self.scrollbar_vertical = ttk.Scrollbar(self, orient='vertical')
        self.scrollbar_horizontal = ttk.Scrollbar(self, orient='horizontal')
        # configure vertical scrollbar
        self.main_canvas.configure(yscrollcommand=self.scrollbar_vertical.set)
        self.scrollbar_vertical.configure(command=self.main_canvas.yview)
        # configure horizontal scrollbar
        self.main_canvas.configure(xscrollcommand=self.scrollbar_horizontal.set)
        self.scrollbar_horizontal.configure(command=self.main_canvas.xview)
        # load content to frame
        i = 1
        for key, value in self.content.items():
            column_name = key
            # init label
            label = tk.Label(self.main_frame, text=column_name)
            # init stringvar to entry
            str_var = tk.StringVar(self.main_frame, value=value)
            # init entry
            entry = tk.Entry(self.main_frame, textvariable=str_var)
            label.grid(row=i, column=0, sticky='we', padx=10)
            entry.grid(row=i+1, column=0, sticky='we', pady=10, padx=10)
            separator = ttk.Separator(self.main_frame, orient='horizontal')
            separator.grid(row=i + 2, column=0, sticky='we', padx=5)
            i += 3
            self.local_values[key] = str_var
            str_var.trace('w', self.value_changed)
        self.organize_widgets()
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas_frame = self.main_canvas.create_window((0, 0), window=self.main_frame, anchor='nw',
                                                           tag='self.canvas_frame')
        self.main_frame.bind("<Configure>", self.on_frame_configure)
        self.main_canvas.bind("<Configure>", self.frame_width)

    def on_frame_configure(self, event) -> None:
        '''Reset the scroll region to include whole inner frame'''
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    def frame_width(self, event):
        canvas_width = event.width
        self.main_canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def _on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def organize_widgets(self) -> None:
        self.main_canvas.grid(row=0, column=0, sticky='nswe')
        self.btn_frame.grid(row=0, column=0, sticky='nw')
        self.btn_save.grid(row=0, column=0, padx=10, sticky='nw')
        self.btn_reset.grid(row=0, column=1, sticky='nw')
        self.scrollbar_vertical.grid(row=0, column=1, sticky='nswe')
        self.scrollbar_horizontal.grid(row=1, column=0, columnspan=2, sticky='we')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_canvas.columnconfigure(0, weight=1)
        self.main_canvas.rowconfigure(0, weight=1)
        self.btn_frame.rowconfigure(0, weight=1)
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(1, weight=1)

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

    def get_iid(self) -> str:
        return self.iid

    def local_save_function(self):
        new_val = self.get_values()
        self.ext_save_function(self.local_values.copy(), new_val, self.iid)
        self.is_content_changed = False

    def value_changed(self, *args):
        if self.is_content_changed is False:
            self.is_content_changed = True

    def reset_changes(self):
        if self.is_content_changed is True:
            for key, value in self.content.items():
                self.local_values[key].set(value)



