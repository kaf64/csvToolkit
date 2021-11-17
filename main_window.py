import tkinter as tk
from tkinter import ttk, filedialog
from csv_reader import CsvReader
from edit_window import EditWindow


class MainWindow(tk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.parent = parent
        self.columns = list()
        self.reader = CsvReader()
        self.init_window()
        self.init_widgets()
        self.organize_widgets()

    def init_window(self) -> None:
        self.parent.title("CSV Toolkit")
        self.parent.state("zoomed")

    def init_widgets(self) -> None:
        self.delimiter_frame = tk.Frame(self.parent)
        self.button_load = tk.Button(self.parent, command=self.open_file_dialog, text='open csv file')
        self.delimiter_label = ttk.Label(self.delimiter_frame, text='delimiter character:')
        self.delimiter_entry = ttk.Entry(self.delimiter_frame, width=1)
        self.delimiter_entry.insert('end', self.reader.get_delimiter())
        self.treeview = ttk.Treeview(self.parent, show='headings')
        self.btn_frame = tk.Frame(self.parent)
        self.btn_show = tk.Button(self.btn_frame, command=self.show_item, text='Show/edit item')
        self.progress_label = ttk.Label(self.parent, text='')

        # add scrollbar to treeview (horizontal and vertical)
        self.treeview_scrollbar_vertical = ttk.Scrollbar(self.parent, orient='vertical')
        self.treeview_scrollbar_horizontal = ttk.Scrollbar(self.parent, orient='horizontal')

        self.treeview.configure(yscrollcommand=self.treeview_scrollbar_vertical.set)
        self.treeview_scrollbar_vertical.configure(command=self.treeview.yview)

        self.treeview.configure(xscrollcommand=self.treeview_scrollbar_horizontal.set)
        self.treeview_scrollbar_horizontal.configure(command=self.treeview.xview)

    def organize_widgets(self) -> None:
        self.parent.grid_propagate(0)
        self.grid_propagate(0)
        self.delimiter_label.grid(row=0, column=0, sticky='w')
        self.delimiter_entry.grid(row=0, column=1, sticky='w')
        self.delimiter_frame.grid(row=0, column=0, sticky='w')
        self.button_load.grid(row=0, column=1, sticky='w')
        # grid
        self.treeview.grid(row=1, column=0, columnspan=2, pady=20, padx=10, sticky='nswe')
        self.treeview.grid_remove()  # hide treeview
        self.treeview_scrollbar_vertical.grid(row=1, column=2, sticky='ns')
        self.treeview_scrollbar_horizontal.grid(row=2, column=0, columnspan=2, sticky='we')
        self.btn_frame.grid(row=3, column=0, columnspan=2, sticky='we')
        self.btn_show.grid(row=0, column=0, sticky='w')
        self.progress_label.grid(row=4, column=0, sticky='w')
        # configure columns
        self.parent.columnconfigure(0, weight=0)
        self.parent.columnconfigure(1, weight=1)
        self.parent.columnconfigure(2, weight=0)
        self.btn_frame.columnconfigure(0, weight=1)
        # configure rows
        self.parent.rowconfigure(0, weight=0)
        self.parent.rowconfigure(1, weight=1)
        self.parent.rowconfigure(2, weight=0)
        self.parent.rowconfigure(3, weight=0)
        self.parent.rowconfigure(4, weight=0)
        self.parent.rowconfigure(5, weight=0)
        self.btn_frame.rowconfigure(0, weight=1)

    def show_item(self):
        #get selected line in treeview
        selected_item = self.treeview.focus()
        selected_item = self.treeview.selection()
        if selected_item is not None and len(selected_item) >= 1:
            # make dictionary from columns and values
            values = self.treeview.item(selected_item)['values']
            item_content = list()
            for i in range(1, len(self.columns)):
                column_dict = {
                    'column_name': self.columns[i],
                    'value': values[i]
                }
                item_content.append(column_dict)
            # init and show new window
            edit_window = EditWindow(self.parent, item_content)

    def open_file_dialog(self) -> None:
        file_path = filedialog.askopenfilename(title='open a file', filetypes=[("csv files", "*.csv")])
        delimiter = self.delimiter_entry.get()
        self.progress_label.config(text=f'prepare to load items')
        self.parent.title("CSV Toolkit - " + str(file_path))
        self.update()
        data = self.reader.read(delimiter, file_path)
        self.load_to_treeview(data)

    def get_dict_to_list(self, dictionary: dict) -> list:
        res = list()
        for key, val in dictionary.items():
            res.append(val)
        return res

    def load_to_treeview(self, content: dict) -> None:
        key_list = content['keys']
        if key_list is not None:
            self.columns = ['item'] + list(key_list)
            self.treeview['columns'] = self.columns
            # configuring first column
            self.treeview.heading('item', text='Item number', anchor='center')
            for key in key_list:
                self.treeview.heading(key, text=key, anchor='center')
            # delete children if exists
            if self.treeview.get_children():
                self.treeview.delete(*self.treeview.get_children())
            data_length = len(content['data'])
            self.treeview.grid()  # show treeview
            for index, data_item in enumerate(content['data']):
                val_list = self.get_dict_to_list(data_item)
                self.treeview.insert(parent='', index=data_item['index'], iid=data_item['index'], text='', values=val_list)
                self.progress_label.config(text=f'loading items: {index+1}/{data_length}')
            self.progress_label.config(text='loading complete')
            self.treeview_scrollbar_vertical.grid(row=1, column=4, rowspan=4, stick='nse')
            self.update()
        else:
            self.progress_label.config(text='file is empty')



