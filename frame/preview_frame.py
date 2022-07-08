import tkinter as tk
from tkinter import ttk
from classes.window.edit_window import EditWindow
from classes.window.add_window import AddWindow
import pandas as pd


class PreviewFrame(tk.Frame):
    def __init__(self, parent_progress_label=tk.Label, parent=tk.Tk):
        super().__init__(parent)
        self.parent = parent
        self.data = None
        self.edit_window = None
        self.add_window = None
        self.progress_label = parent_progress_label
        # init widgets
        # treeview
        self.treeview = ttk.Treeview(self, show='headings')
        # bind function to double click event
        self.treeview.bind("<Double-1>", self.show_item)
        # button frame
        self.btn_frame = tk.Frame(self)
        # show edit item btn
        self.btn_show = tk.Button(self.btn_frame, command=lambda: self.show_item(None), text='Show/edit item')
        # add new item btn
        self.btn_add = tk.Button(self.btn_frame, command=lambda: self.add_new_item_dialog(), text='Add new item')
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
        self.treeview.grid(row=0, column=0, sticky='nswe')
        self.treeview.grid_remove()  # hide treeview
        self.treeview_scrollbar_vertical.grid(row=0, column=1, sticky='ns')
        self.treeview_scrollbar_horizontal.grid(row=1, column=0, sticky='we')
        self.btn_frame.grid(row=3, column=0, columnspan=2, sticky='we')
        self.btn_show.grid(row=0, column=0, padx=10, sticky='w')
        self.btn_add.grid(row=0, column=1, padx=10, sticky='w')

        # configure columns
        self.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(0, weight=0)
        self.btn_frame.columnconfigure(1, weight=0)
        self.btn_frame.columnconfigure(1, weight=1)
        # configure rows
        self.rowconfigure(0, weight=1)
        self.btn_frame.rowconfigure(0, weight=1)

    def refresh_widgets(self):
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
        self.treeview.grid(row=0, column=0, sticky='nswe')

    def init_data(self, data: pd.DataFrame) -> None:
        self.data = data
        if self.treeview is not None:
            self.reset_treeview()
            self.load_to_treeview(self.data)
        self.treeview.grid()  # show treeview

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
                parent=self.parent, content=item_content.copy(), external_fn=self.update_item, iid=selected_item)
            self.edit_window.protocol("WM_DELETE_WINDOW",
                                      lambda: self.exit_dialog(window_type='edit', active_window=self.edit_window))

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

    def update_item(self, local_values, new_values, index) -> None:
        for key, val in new_values.items():
            local_values[key] = val
        # get treeview item do update
        item_to_update = self.treeview.index(index)
        # update dataframe
        self.data.loc[int(index), :] = new_values.values()
        # update treeivew item
        self.treeview.item(item_to_update, values=list(local_values.values()))

    def add_new_item_dialog(self) -> None:
        if self.data.columns is not None and self.edit_window is None:
            # make dictionary from columns and values
            item_content = {column: " " for column in self.data.columns}
            # init and show new window
            self.add_window = AddWindow(
                parent=self.parent, external_fn=self.add_new_item, content=item_content)
            self.add_window.protocol("WM_DELETE_WINDOW",
                                     lambda: self.exit_dialog(window_type='add', active_window=self.add_window))

    def add_new_item(self, new_values: dict) -> None:
        new_item = pd.Series(data=new_values.values(), index=self.data.columns)
        # new_item.columns = self.data.columns
        # for key, val in new_values.items():
        #    new_item[key] = val
        self.data = pd.concat(objs=[self.data, new_item.to_frame().T], ignore_index=True)
        #self.data.concat(new_item)
        # update treeview item
        self.refresh_widgets()

