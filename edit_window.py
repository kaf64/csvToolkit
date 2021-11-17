import tkinter as tk
from tkinter import ttk, messagebox


class EditWindow(tk.Toplevel):
    def __init__(self, parent: tk.Tk, content: list) -> None:
        super().__init__(parent)
        self.content = content
        self.title('Show/edit item')
        self.main_canvas = tk.Canvas(self, borderwidth=0)
        self.main_frame = tk.Frame(self.main_canvas)
        # add scrollbar
        self.scrollbar_vertical = ttk.Scrollbar(self, orient='vertical')
        self.scrollbar_horizontal = ttk.Scrollbar(self, orient='horizontal')
        # configure vertical scrollbar
        self.main_canvas.configure(yscrollcommand=self.scrollbar_vertical.set)
        self.scrollbar_vertical.configure(command=self.main_canvas.yview)
        # configure horizontal scrollbar
        self.main_canvas.configure(xscrollcommand=self.scrollbar_horizontal.set)
        self.scrollbar_horizontal.configure(command=self.main_canvas.xview)
        # init list of local values StringVars type
        self.local_values = list()
        # load content to frame
        i = 0
        for item in self.content:
            column_name = item['column_name']
            # init label
            label = tk.Label(self.main_frame, text=column_name)
            # init stringvar to entry
            str_var = tk.StringVar(self.main_frame, value=item['value'])
            # init entry
            entry = tk.Entry(self.main_frame, textvariable=str_var)
            label.grid(row=i, column=0, sticky='we', padx=10)
            entry.grid(row=i+1, column=0, sticky='we', pady=10, padx=10)
            separator = ttk.Separator(self.main_frame, orient='horizontal')
            separator.grid(row=i + 2, column=0, sticky='we', padx=5)
            i += 3
            local_entry = {
                'column_name': column_name,
                'value': str_var
            }
            self.local_values.append(local_entry)
        self.organize_widgets()
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas_frame = self.main_canvas.create_window((0, 0), window=self.main_frame, anchor='nw',
                                                           tag='self.canvas_frame')
        self.main_frame.bind("<Configure>", self.on_frame_configure)
        self.main_canvas.bind("<Configure>", self.frame_width)

    def on_frame_configure(self, event) -> None:
        '''Reset the scroll region to encompass the inner frame'''
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    def frame_width(self, event):
        canvas_width = event.width
        self.main_canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def _on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def organize_widgets(self) -> None:
        self.main_canvas.grid(row=0, column=0, sticky='nswe')
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
