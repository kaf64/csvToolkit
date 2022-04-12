import tkinter as tk
from tkinter import ttk
import pandas as pd
import plotly.express as px
import plotly.io as pio


class PlotFrame(tk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
        pio.renderers.default = 'browser'
        super().__init__(parent)
        self.data = None
        self.var_style_static = tk.StringVar(value='line')
        self.var_style_interactive = tk.StringVar(value='line')
        # init widgets
        self.label_x_axis = tk.Label(self, text="Select column as X axis")
        self.label_x_axis.grid(row=0, column=0)
        self.listbox_x = ttk.Combobox(self)
        self.listbox_x.grid(row=0, column=1)
        self.label_y_axis = tk.Label(self, text="Select column as Y axis")
        self.label_y_axis.grid(row=1, column=0)
        self.listbox_y = ttk.Combobox(self)
        self.listbox_y.grid(row=1, column=1)
        self.plot_title_var = tk.StringVar(value='')
        self.plot_title_label = tk.Label(self, text='Set plot title (optional)')
        self.plot_title_label.grid(row=2, column=0)
        self.plot_title_entry = tk.Entry(self, textvariable=self.plot_title_var)
        self.plot_title_entry.grid(row=2, column=1)
        self.frame_graph_type = self.init_graph_type_widgets()
        self.frame_graph_type.grid(row=3, column=0, sticky='we')
        self.button_plot_static = tk.Button(self, text="Generate plot in new window",
                                            command=lambda: self.generate_plot_static(
                                                plot_type=self.var_style_static.get()))
        self.button_plot_static.grid(row=4, column=0)
        self.button_plot_interactive = tk.Button(self, text="Generate interactive plot in browser",
                                                 command=lambda: self.generate_plot_interactive(
                                                     plot_type=self.var_style_interactive.get()))
        self.button_plot_interactive.grid(row=4, column=1)

    def refresh_widgets(self):
        column_list = self.data.columns.values.tolist()
        self.listbox_x['values'] = column_list
        self.listbox_y['values'] = column_list

    def init_graph_type_widgets(self):
        frame = tk.Frame(self)
        # static types
        # line, pie, histogram
        # setting default type
        self.var_style_static.value = 'line'
        label_style_static = tk.Label(frame, text='Select static plot type')
        label_style_static.grid(row=0, column=0)
        radio_select_static_line = tk.Radiobutton(frame, text="line", variable=self.var_style_static,
                            value='line')
        radio_select_static_line.grid(row=1, column=0, sticky='w')
        radio_select_static_line = tk.Radiobutton(frame, text="pie", variable=self.var_style_static,
                            value='pie')
        radio_select_static_line.grid(row=2, column=0, sticky='w')
        radio_select_static_line = tk.Radiobutton(frame, text="histogram", variable=self.var_style_static,
                            value='hist')
        radio_select_static_line.grid(row=3, column=0, sticky='w')
        radio_select_static_line = tk.Radiobutton(frame, text="bar", variable=self.var_style_static,
                            value='bar')
        radio_select_static_line.grid(row=4, column=0, sticky='w')
        radio_select_static_line = tk.Radiobutton(frame, text="horizontal bar", variable=self.var_style_static,
                            value='barh')
        radio_select_static_line.grid(row=5, column=0, sticky='w')
        # set divider
        separator = ttk.Separator(frame, orient='vertical')
        separator.grid(row=0, column=1, rowspan=5, sticky='ns', pady=10, padx=10)
        # interactive types
        # scatter,paralell coordinates, line
        # setting default type
        self.var_style_interactive.value = 'line'
        label_style_interactive = tk.Label(frame, text='Select interactive plot type')
        label_style_interactive.grid(row=0, column=2, sticky='w')
        radio_select_static_line = tk.Radiobutton(frame, text="scatter", variable=self.var_style_interactive,
                            value='scatter')
        radio_select_static_line.grid(row=1, column=2, sticky='w')
        radio_select_static_line = tk.Radiobutton(frame, text="paralell coordinates",
                                                  variable=self.var_style_interactive,
                                                  value='parallell_coordinates')
        radio_select_static_line.grid(row=2, column=2, sticky='w')
        radio_select_static_line = tk.Radiobutton(frame, text="line",
                                                  variable=self.var_style_interactive,
                                                  value='line')
        radio_select_static_line.grid(row=3, column=2, sticky='w')
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        return frame

    def init_data(self, data: pd.DataFrame) -> None:
        self.data = data
        column_list = self.data.columns.values.tolist()
        self.listbox_x['values'] = column_list
        self.listbox_y['values'] = column_list

    def generate_plot_interactive(self, plot_type: str):
        column_x_str = str(self.listbox_x.get())
        column_y_str = str(self.listbox_y.get())
        title = self.plot_title_var.get()
        fig = None
        if plot_type == 'line':
            fig = px.line(data_frame=self.data, x=column_x_str, y=column_y_str, title=title)
        elif plot_type == 'scatter':
            fig = px.scatter(data_frame=self.data, x=column_x_str, y=column_y_str, title=title)
        elif plot_type == 'parallell_coordinates':
            fig = px.parallel_coordinates(data_frame=self.data, title=title)
        elif plot_type == 'parallell_categories':
            fig = px.parallel_categories(data_frame=self.data, title=title)
        fig.show()

    def generate_plot_static(self, plot_type: str):
        column_x_str = str(self.listbox_x.get())
        column_y_str = str(self.listbox_y.get())
        title = str(self.plot_title_var.get())
        plot_img = self.data.plot(x=column_x_str, y=column_y_str, kind=plot_type, title=title)
        plot_img.figure.show()


