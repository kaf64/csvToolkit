import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from classes.window.edit_window import EditWindow
from classes.window.add_window import AddWindow
from classes.window.add_column_window import AddColumnWindow
from classes.window.delete_column_window import DeleteColumnWindow
from classes.data_interface.data_interface import DataInterface
import pandas as pd


class PreviewFrame(tk.Frame):
    def __init__(self, parent_progress_label=tk.Label, parent=tk.Tk):
        super().__init__(parent)
        self.parent = parent
        self.data = pd.DataFrame()
        self.data_interface = DataInterface()
        self.edit_window = None
        self.add_window = None
        self.add_column_window = None
        self.delete_column_window = None
        self.progress_label = parent_progress_label
        # init widgets
        # treeview
        self.treeview = ttk.Treeview(self, show='headings')
        # bind function to double click event
        self.treeview.bind("<Double-1>", self.show_item)
        # button frame
        self.btn_frame = tk.Frame(self)
        # search bar frame
        self.search_frame = tk.Frame(self)
        # show edit item btn
        self.btn_show = tk.Button(self.btn_frame, command=lambda: self.show_item(None), text='Show/edit item')
        # add new item btn
        self.btn_add = tk.Button(self.btn_frame, command=lambda: self.add_new_item_dialog(), text='Add new item')
        # add new column btn
        self.btn_add_column = tk.Button(self.btn_frame, command=lambda: self.add_new_column_dialog(),
                                        text='Add new column')
        self.btn_del_column = tk.Button(self.btn_frame, command=lambda: self.delete_column_dialog(),
                                        text='Delete column')
        self.btn_del_row = tk.Button(self.btn_frame, command=lambda: self.delete_item(),
                                        text='Delete selected row(s)')
        # create widgets to search frame
        self.search_label = tk.Label(self.search_frame, text="Value to search: ")
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.bind("<Return>", lambda event=None: self.search_btn_start.invoke())
        self.search_btn_start = tk.Button(self.search_frame, command=lambda: self.search_start(), text='Start search')
        self.search_btn_reset = tk.Button(self.search_frame, command=lambda: self.search_reset(), text='Reset search')
        # add scrollbar to treeview (horizontal and vertical)
        self.treeview_scrollbar_vertical = ttk.Scrollbar(self, orient='vertical')
        self.treeview_scrollbar_horizontal = ttk.Scrollbar(self, orient='horizontal')
        # configure vertical scrollbar
        self.treeview.configure(yscrollcommand=self.treeview_scrollbar_vertical.set)
        self.treeview_scrollbar_vertical.configure(command=self.treeview.yview)
        # configure horizontal scrollbar
        self.treeview.configure(xscrollcommand=self.treeview_scrollbar_horizontal.set)
        self.treeview_scrollbar_horizontal.configure(command=self.treeview.xview)
        # organize widgets
        self.search_frame.grid(row=0, column=0, sticky='we')
        self.search_label.grid(row=0, column=0, sticky='w')
        self.search_entry.grid(row=0, column=1, sticky='we')
        self.search_btn_start.grid(row=0, column=3, sticky='e')
        self.search_btn_reset.grid(row=0, column=4, sticky='e')
        self.treeview.grid(row=1, column=0, sticky='nsew')
        self.treeview.grid_remove()  # hide treeview
        self.treeview_scrollbar_vertical.grid(row=1, column=1, sticky='ns')
        self.treeview_scrollbar_horizontal.grid(row=2, column=0, sticky='we')
        self.btn_frame.grid(row=4, column=0, columnspan=2, sticky='we')
        self.btn_show.grid(row=0, column=0, padx=10, sticky='w')
        self.btn_add.grid(row=0, column=1, padx=10, sticky='w')
        self.btn_add_column.grid(row=0, column=2, padx=10, sticky='w')
        self.btn_del_column.grid(row=0, column=3, padx=10, sticky='w')
        self.btn_del_row.grid(row=0, column=4, padx=10, sticky='w')
        # configure columns
        self.columnconfigure(0, weight=1)
        self.search_frame.columnconfigure(0, weight=0)
        self.search_frame.columnconfigure(1, weight=1)
        self.search_frame.columnconfigure(2, weight=0)
        self.search_frame.columnconfigure(3, weight=0)
        self.btn_frame.columnconfigure(0, weight=0)
        self.btn_frame.columnconfigure(1, weight=0)
        self.btn_frame.columnconfigure(2, weight=0)
        self.btn_frame.columnconfigure(3, weight=0)
        self.btn_frame.columnconfigure(4, weight=0)
        self.btn_frame.columnconfigure(5, weight=1)
        # configure rows
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.btn_frame.rowconfigure(0, weight=1)
        self.search_frame.rowconfigure(0, weight=1)

    def refresh_widgets(self, *args):
        if self.data is not None:
            self.reset_treeview()
            self.load_to_treeview(self.data)

    def reset_treeview(self):
        # destroy treeview and make new to prevent change width of widget
        self.treeview.destroy()
        self.treeview = ttk.Treeview(self, show='headings')
        # bind function to double click event
        self.treeview.bind("<Double-1>", self.show_item)
        self.treeview.configure(yscrollcommand=self.treeview_scrollbar_vertical.set)
        self.treeview_scrollbar_vertical.configure(command=self.treeview.yview)
        # configure horizontal scrollbar
        self.treeview.configure(xscrollcommand=self.treeview_scrollbar_horizontal.set)
        self.treeview_scrollbar_horizontal.configure(command=self.treeview.xview)
        self.treeview.grid(row=1, column=0, sticky='nsew')

    def init_data(self, data: pd.DataFrame) -> None:
        self.data = data
        self.data_interface.init_data(data_to_init=self.data)
        if self.treeview is not None:
            self.reset_treeview()
            self.load_to_treeview(self.data)
        #self.treeview.grid()  # show treeview

    def show_item(self, event: None):
        #get selected line in treeview
        selected_item = self.treeview.focus()
        index = self.treeview.index(selected_item)
        if selected_item is not None and len(selected_item) >= 1 and self.edit_window is None:
            # make dictionary from columns and values
            values = self.treeview.item(selected_item)['values']
            item_content = self.data.iloc[index].to_dict()
            # init and show new window
            self.edit_window = EditWindow(
                parent=self.parent, content=item_content.copy(), iid=selected_item, data_interface=self.data_interface)
            self.edit_window.protocol("WM_DELETE_WINDOW",
                                      lambda: self.exit_dialog(window_type='edit', active_window=self.edit_window))
            self.edit_window.bind("<<DataUpdate>>", self.refresh_widgets)

    def exit_dialog(self, window_type: str, active_window) -> None:
        if window_type == "edit":
            is_changed = self.edit_window.get_is_content_changed()
        elif window_type == "add":
            is_changed = self.add_window.get_is_content_changed()
        if is_changed:
            message = 'Do you want save changes before close?'
            user_decision = tk.messagebox.askyesnocancel(parent=active_window, title='close', message=message)
            if user_decision is None:
                return
            elif user_decision is True:
                if window_type == "add":
                    new_values = self.add_window.get_values()
                    self.add_new_item(new_values)
                elif window_type == "edit":
                    new_values_list = self.edit_window.get_values()
                    iid = self.edit_window.get_iid()
                    self.update_item(self.data.iloc[iid], new_values_list, iid)
        if is_changed is False or user_decision is False:
            if window_type == "add":
                self.add_window.destroy()
                self.add_window = None
            elif window_type == "edit":
                self.edit_window.destroy()
                self.edit_window = None
            elif window_type == 'add_column':
                self.add_column_window.destroy()
                self.add_column_window = None

    def load_to_treeview(self, content: pd.DataFrame) -> None:
        columns = content.columns
        if columns is not None:
            if self.treeview.get_children():
                self.treeview.delete(*self.treeview.get_children())
            self.treeview['columns'] = list(columns)
            for col in columns:
                self.treeview.heading(col, text=col, anchor='center')
            # delete children if exists
            for index, row in content.iterrows():
                val_list = row.tolist()
                self.treeview.insert(parent='', index=tk.END, iid=index, text='', values=val_list)
            self.progress_label.config(text='loading complete')
        else:
            self.progress_label.config(text='file is empty')
        self.update()

    def update_item(self, new_values, index) -> None:
        # update dataframe
        self.data.loc[int(index), :] = new_values.values()

    def update_treeview_item(self, index, new_values):
        # update treeview item
        item_to_update = self.treeview.index(index)
        self.treeview.item(item_to_update, values=list(new_values))

    def add_new_item_dialog(self) -> None:
        if self.data.columns is not None and self.add_window is None:
            # make dictionary from columns and values
            item_content = {column: " " for column in self.data.columns}
            # init and show new window
            self.add_window = AddWindow(
                parent=self.parent, data_interface=self.data_interface, content=item_content)
            self.add_window.protocol("WM_DELETE_WINDOW",
                                     lambda: self.exit_dialog(window_type='add', active_window=self.add_window))
            self.add_window.bind("<<DataUpdate>>", self.refresh_widgets)

    def add_new_column_dialog(self) -> None:
        if self.data.columns is not None and self.add_column_window is None:
            # init and show new window
            self.add_column_window = AddColumnWindow(
                parent=self.parent, data_interface=self.data_interface)
            self.add_column_window.protocol("WM_DELETE_WINDOW",
                                      lambda: self.exit_dialog(window_type='add_column', active_window=None))
            self.add_column_window.bind("<<DataUpdate>>", self.refresh_widgets)

    def delete_column_dialog(self) -> None:
        if self.data.columns is not None and self.delete_column_window is None:
            # init and show new window
            self.delete_column_window = DeleteColumnWindow(
                parent=self.parent, data_interface=self.data_interface, columns=self.data.columns.to_list())
            self.delete_column_window.bind("<<DataUpdate>>", self.refresh_widgets)

    def delete_item(self) -> None:
        # get selected row in treeview
        selected_item = self.treeview.selection()
        if selected_item is not None:
            message = "Are you sure to delete selected row(s)?"
            user_decision = tk.messagebox.askyesnocancel(parent=self, title='close', message=message)
            if user_decision is None or user_decision is False:
                return
            elif user_decision is True:
                if len(selected_item) == 1:
                    index = self.treeview.index(selected_item)
                    self.data_interface.delete_item(index=index)
                elif len(selected_item) >= 2:
                    for index_item in selected_item:
                        index = self.treeview.index(index_item)
                        self.data_interface.delete_item(index=index)
                self.refresh_widgets()

    def search_start(self):
        value = self.search_entry.get()
        if value != '' and self.data is not None:
            result = self.data_interface.find_value(value=str(value))
            self.reset_treeview()
            self.load_to_treeview(content=result)

    def search_reset(self):
        self.search_entry.delete(0, tk.END)
        self.reset_treeview()
        self.load_to_treeview(content=self.data)


