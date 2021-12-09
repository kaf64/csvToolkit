import tkinter as tk
from tkinter import ttk, filedialog
from csv_reader import CsvReader
from csv_writer import CsvWriter
from edit_window import EditWindow


class MainWindow(tk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.parent = parent
        self.data = None
        self.columns = list()
        self.reader = CsvReader()
        self.writer = CsvWriter()
        self.init_window()
        self.init_widgets()
        self.organize_widgets()

    def init_window(self) -> None:
        self.parent.title("CSV Toolkit")
        self.parent.state("zoomed")

    def init_widgets(self) -> None:
        self.button_load = tk.Button(self.parent, command=self.open_file_dialog, text='Open csv file')
        # init delimiter frame and widgets
        self.delimiter_frame = tk.Frame(self.parent)
        self.delimiter_label = ttk.Label(self.delimiter_frame, text='delimiter character:')
        self.delimiter_entry = ttk.Entry(self.delimiter_frame, width=1)
        # init notebook widgets and frames
        self.notebook = ttk.Notebook(self.parent)
        self.frame_preview = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_preview, text='Preview')
        self.delimiter_entry.insert('end', self.reader.get_delimiter())
        self.treeview = ttk.Treeview(self.frame_preview, show='headings')
        self.btn_frame = tk.Frame(self.parent)
        self.btn_show = tk.Button(self.btn_frame, command=lambda: self.show_item(None), text='Show/edit item')
        self.btn_save = tk.Button(self.btn_frame, command=self.save_data, text='Save file')
        self.progress_label = ttk.Label(self.parent, text='')

        # add scrollbar to treeview (horizontal and vertical)
        self.treeview_scrollbar_vertical = ttk.Scrollbar(self.parent, orient='vertical')
        self.treeview_scrollbar_horizontal = ttk.Scrollbar(self.parent, orient='horizontal')

        self.treeview.configure(yscrollcommand=self.treeview_scrollbar_vertical.set)
        self.treeview_scrollbar_vertical.configure(command=self.treeview.yview)

        self.treeview.configure(xscrollcommand=self.treeview_scrollbar_horizontal.set)
        self.treeview_scrollbar_horizontal.configure(command=self.treeview.xview)
        self.edit_window = None
        self.treeview.bind("<Double-1>", self.show_item)

    def organize_widgets(self) -> None:
        self.parent.grid_propagate(0)
        self.grid_propagate(0)
        self.delimiter_label.grid(row=0, column=0, sticky='w')
        self.delimiter_entry.grid(row=0, column=1, sticky='w')
        self.delimiter_frame.grid(row=0, column=0, sticky='w')
        self.button_load.grid(row=0, column=1, sticky='w')
        # grid
        self.notebook.grid(row=1, column=0, columnspan=2, pady=20, padx=10, sticky='nswe')
        self.treeview.grid(row=0, column=0, sticky='nswe')
        self.treeview.grid_remove()  # hide treeview
        self.treeview_scrollbar_vertical.grid(row=1, column=2, sticky='ns')
        self.treeview_scrollbar_horizontal.grid(row=2, column=0, columnspan=2, sticky='we')
        self.btn_frame.grid(row=3, column=0, columnspan=2, sticky='we')
        self.btn_show.grid(row=0, column=0, padx=10, sticky='w')
        self.btn_save.grid(row=0, column=1, sticky='w')
        self.progress_label.grid(row=4, column=0, sticky='w')
        # configure columns
        self.parent.columnconfigure(0, weight=0)
        self.parent.columnconfigure(1, weight=1)
        self.parent.columnconfigure(2, weight=0)
        self.btn_frame.columnconfigure(0, weight=0)
        self.btn_frame.columnconfigure(1, weight=0)
        self.btn_frame.columnconfigure(1, weight=1)
        self.frame_preview.columnconfigure(0, weight=1)

        # configure rows
        self.parent.rowconfigure(0, weight=0)
        self.parent.rowconfigure(1, weight=1)
        self.parent.rowconfigure(2, weight=0)
        self.parent.rowconfigure(3, weight=0)
        self.parent.rowconfigure(4, weight=0)
        self.parent.rowconfigure(5, weight=0)
        self.btn_frame.rowconfigure(0, weight=1)
        self.frame_preview.rowconfigure(0, weight=1)

    def show_item(self, event: None):
        #get selected line in treeview
        selected_item = self.treeview.focus()
        if selected_item is not None and len(selected_item) >= 1 and self.edit_window is None:
            # make dictionary from columns and values
            values = self.treeview.item(selected_item)['values']
            item_content = self.data[int(selected_item)]
            # init and show new window
            self.edit_window = EditWindow(
                parent=self.parent, content=item_content.copy(), external_fn=self.update_item, iid=selected_item)
            self.edit_window.protocol("WM_DELETE_WINDOW", lambda: self.exit_dialog())

    def exit_dialog(self):
        is_changed = self.edit_window.get_is_content_changed()
        if is_changed:
            message = 'Do you want save changes before close?'
            user_decision = tk.messagebox.askyesnocancel(parent=self.edit_window, title='close', message=message)
            if user_decision is None:
                return
            elif user_decision is True:
                new_values_list = self.edit_window.get_values()
                iid = self.edit_window.get_iid()
                self.update_item(self.data[int(iid)], new_values_list, iid)
            self.edit_window.destroy()
            self.edit_window = None

    def update_item(self, local_values, new_values, index):
        for key, val in new_values.items():
            local_values[key] = val
        # get treeview item do update
        item_to_update = self.treeview.index(index)
        # update treeivew item
        self.treeview.item(item_to_update, values=self.get_dict_to_list(local_values))
        return

    def open_file_dialog(self) -> None:
        filetypes = [("csv files", "*.csv")]
        file_path = filedialog.askopenfilename(title='open a file', filetypes=filetypes)
        delimiter = self.delimiter_entry.get()
        self.progress_label.config(text=f'prepare to load items')
        self.parent.title("CSV Toolkit - " + str(file_path))
        self.update()
        res = self.reader.read(delimiter, file_path)
        self.data = res['data']
        self.columns = res['keys']
        self.load_to_treeview(self.data)

    def save_data(self) -> None:
        filetypes = [("csv files", "*.csv")]
        file_path = filedialog.asksaveasfilename(title='save file', filetypes=filetypes, defaultextension=".csv")
        delimiter = self.delimiter_entry.get()
        self.progress_label.config(text=f'saving item ...')
        self.writer.write(file_path=file_path, data=self.data, columns=self.columns)
        self.progress_label.config(text=f'file saved')

    def get_dict_to_list(self, dictionary: dict) -> list:
        res = list()
        for key, val in dictionary.items():
            res.append(val)
        return res

    def load_to_treeview(self, content: dict) -> None:
        key_list = self.columns
        if key_list is not None:
            self.columns = list(key_list)
            self.treeview['columns'] = self.columns
            for key in key_list:
                self.treeview.heading(key, text=key, anchor='center')
            # delete children if exists
            if self.treeview.get_children():
                self.treeview.delete(*self.treeview.get_children())
            data_length = len(content)
            self.treeview.grid()  # show treeview
            for index, data_item in enumerate(content):
                val_list = self.get_dict_to_list(data_item)
                self.treeview.insert(parent='', index=tk.END, iid=index, text='', values=val_list)
                self.progress_label.config(text=f'loading items: {index+1}/{data_length}')
            self.progress_label.config(text='loading complete')
            self.treeview_scrollbar_vertical.grid(row=1, column=4, rowspan=4, stick='nse')
            self.update()
        else:
            self.progress_label.config(text='file is empty')



