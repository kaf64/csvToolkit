import tkinter as tk
from tkinter import ttk, filedialog
from edit_window import EditWindow
import pandas as pd


class PreviewFrame(tk.Frame):
    def __init__(self, parent_progress_label=tk.Label, parent=tk.Tk):
        super().__init__(parent)
        self.parent = parent
        self.data = None
        self.edit_window = None
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
        # configure columns
        self.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(0, weight=0)
        self.btn_frame.columnconfigure(1, weight=0)
        self.btn_frame.columnconfigure(1, weight=1)
        # configure rows
        self.rowconfigure(0, weight=1)
        self.btn_frame.rowconfigure(0, weight=1)

    def init_data(self, data: pd.DataFrame) -> None:
        self.data = data
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
                self.update_item(self.data.iloc[iid], new_values_list, iid)
        self.edit_window.destroy()
        self.edit_window = None

    def load_to_treeview(self, content: pd.DataFrame) -> None:
        columns = content.columns
        if columns is not None:
            self.treeview['columns'] = list(columns)
            for col in columns:
                self.treeview.heading(col, text=col, anchor='center')
            # delete children if exists
            if self.treeview.get_children():
                self.treeview.delete(*self.treeview.get_children())
            data_length = len(content)
            for index, row in content.iterrows():
                val_list = row.tolist()
                self.treeview.insert(parent='', index=tk.END, iid=index, text='', values=val_list)
            self.progress_label.config(text='loading complete')
        else:
            self.progress_label.config(text='file is empty')

    def update_item(self, local_values, new_values, index) -> None:
        for key, val in new_values.items():
            local_values[key] = val
        # get treeview item do update
        item_to_update = self.treeview.index(index)
        # update dataframe
        self.data.loc[int(index), :] = new_values.values()
        # update treeivew item
        self.treeview.item(item_to_update, values=self.get_dict_to_list(local_values))

    def get_dict_to_list(self, dictionary: dict) -> list:
        res = list()
        for key, val in dictionary.items():
            res.append(val)
        return res
