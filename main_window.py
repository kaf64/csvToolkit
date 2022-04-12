import tkinter as tk
from tkinter import ttk, filedialog
from csv_reader import CsvReader
from csv_writer import CsvWriter
from frame.preview_frame import PreviewFrame
from frame.plot_frame import PlotFrame
from frame.process_frame import ProcessFrame
import pandas as pd


class MainWindow(tk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.parent = parent
        self.data = None
        self.reader = CsvReader()
        self.writer = CsvWriter()
        self.init_window()
        self.init_widgets()
        self.organize_widgets()

    def init_window(self) -> None:
        self.parent.title("CSV Toolkit")
        self.parent.state("zoomed")

    def init_widgets(self) -> None:
        self.progress_label = ttk.Label(self.parent, text='')
        self.frame_btn = ttk.Frame(self.parent)
        self.button_load = tk.Button(self.frame_btn, command=self.open_file_dialog, text='Open csv file')
        self.button_save = tk.Button(self.frame_btn, command=self.save_data, text='Save file')
        # init delimiter frame and widgets
        self.frame_delimiter = tk.Frame(self.parent)
        self.delimiter_label = ttk.Label(self.frame_delimiter, text='delimiter character:')
        self.delimiter_entry = ttk.Entry(self.frame_delimiter, width=1)
        # init notebook widgets and frames
        self.notebook = ttk.Notebook(self.parent)
        self.frame_preview = PreviewFrame(parent_progress_label=self.progress_label, parent=self.notebook)
        self.frame_process = ProcessFrame(parent=self.notebook)
        self.frame_plot = PlotFrame(parent=self.notebook)
        # adding frames to notebook
        self.notebook.add(self.frame_preview, text='Preview')
        self.notebook.add(self.frame_process, text='Process')
        self.notebook.add(self.frame_plot, text='Plot')
        # bind event
        self.notebook.bind("<<NotebookTabChanged>>", self.update_nbframe)
        # init widgets to preview frame
        self.delimiter_entry.insert('end', self.reader.get_delimiter())

    def organize_widgets(self) -> None:
        self.parent.grid_propagate(0)
        self.grid_propagate(0)
        self.delimiter_label.grid(row=0, column=0, sticky='w')
        self.delimiter_entry.grid(row=0, column=1, sticky='w')
        self.frame_delimiter.grid(row=0, column=0, sticky='w')
        self.frame_btn.grid(row=0, column=1, sticky='w')
        self.button_load.grid(row=0, column=0, sticky='w')
        self.button_save.grid(row=0, column=1, sticky='w', padx=10)
        # grid
        self.notebook.grid(row=1, column=0, columnspan=2, pady=20, padx=10, sticky='nswe')
        self.progress_label.grid(row=4, column=0, sticky='w')
        # configure columns
        self.parent.columnconfigure(0, weight=0)
        self.parent.columnconfigure(1, weight=1)
        self.parent.columnconfigure(2, weight=0)
        self.frame_preview.columnconfigure(0, weight=1)
        # configure rows
        self.parent.rowconfigure(0, weight=0)
        self.parent.rowconfigure(1, weight=1)
        self.parent.rowconfigure(2, weight=0)
        self.parent.rowconfigure(3, weight=0)
        self.parent.rowconfigure(4, weight=0)
        self.parent.rowconfigure(5, weight=0)

    def update_nbframe(self, *args) -> None:
        selected_frame = self.notebook.index(self.notebook.select())
        if selected_frame == 0:
            self.frame_preview.refresh_widgets()
        elif selected_frame == 1:
            self.frame_process.refresh_widgets()
        elif selected_frame == 2:
            self.frame_plot.refresh_widgets()

    def open_file_dialog(self) -> None:
        filetypes = [("csv files", "*.csv")]
        file_path = filedialog.askopenfilename(title='open a file', filetypes=filetypes)
        delimiter = self.delimiter_entry.get()
        self.progress_label.config(text=f'prepare to load items')
        self.parent.title("CSV Toolkit - " + str(file_path))
        self.update()
        res = self.reader.read(delimiter, file_path)
        self.data = res
        self.load_widgets_data(content=self.data)

    def load_widgets_data(self, content: pd.DataFrame) -> None:
        self.frame_preview.init_data(data=content)
        self.frame_process.init_data(data=content)
        self.frame_plot.init_data(data=content)

    def save_data(self) -> None:
        filetypes = [("csv files", "*.csv")]
        file_path = filedialog.asksaveasfilename(title='save file', filetypes=filetypes, defaultextension=".csv")
        delimiter = self.delimiter_entry.get()
        self.progress_label.config(text=f'saving item ...')
        self.writer.write(file_path=file_path, data=self.data)
        self.progress_label.config(text=f'file saved')


