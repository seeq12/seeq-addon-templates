import warnings
import ipyvuetify as v
import ipywidgets as widgets
import pandas as pd
import plotly.graph_objects as go
from IPython.display import HTML, clear_output, display

from . import create_new_signal, df_plot, pull_only_signals
from ._backend import push_signal
from ._utils import get_workbook_worksheet_workstep_ids, get_worksheet_url
from seeq.addons.sosg.ui_components import AppLayout

warnings.filterwarnings('ignore')


class MyAddOn(AppLayout):
    def __init__(self, sdl_notebook_url):
        self.workbook_id, self.worksheet_id, self.workstep_id = get_workbook_worksheet_workstep_ids(
            sdl_notebook_url)
        self.worksheet_url = get_worksheet_url(sdl_notebook_url)
        self.df = pull_only_signals(self.worksheet_url)
        self.result_signal = pd.DataFrame()
        clear_output()

        self.signal_plot = go.FigureWidget()

        super(MyAddOn, self).__init__(first_signal_on_change=self.first_signal_dropdown,
                                      second_signal_on_change=self.second_signal_dropdown,
                                      math_operator_on_change=self.math_operator_dropdown
                                      )
        self.first_dropdown_items = list(self.df.columns)
        self.second_dropdown_items = list(self.df.columns)
        self.create_displayed_fig(df_plot(pd.DataFrame))

    def create_displayed_fig(self, fig):
        if fig is None:
            self.visualization = 'message'
            return
        self.visualization = 'plot'
        self.signal_plot = go.FigureWidget(fig)

    def math_operation(self):
        if self.math_operator_value == '+':
            return 'add'
        if self.math_operator_value == '-':
            return 'subtract'
        if self.math_operator_value == 'x':
            return 'multiply'
        if self.math_operator_value == '/':
            return 'divide'

    def first_signal_dropdown(self, data):
        # ipyvuetify doesn't assign the value of the component till the end of the callback. Thus, assigned manually
        self.first_dropdown_value = data
        self.update_display()

    def second_signal_dropdown(self, data):
        # ipyvuetify doesn't assign the value of the component till the end of the callback. Thus, assigned manually
        self.second_dropdown_value = data
        self.update_display()

    def math_operator_dropdown(self, data):
        # ipyvuetify doesn't assign the value of the component till the end of the callback. Thus, assigned manually
        self.math_operator_value = data
        self.update_display()

    def update_display(self, *_):
        self.result_signal = pd.DataFrame()
        self.disabled_controls = True
        fig = None
        if {self.first_dropdown_value, self.second_dropdown_value}.issubset(set(self.df.columns)):
            self.result_signal = create_new_signal(self.df[self.first_dropdown_value].values,
                                                   self.df[self.second_dropdown_value].values,
                                                   self.df.index,
                                                   self.math_operation())
        self.disabled_controls = False
        fig = df_plot(self.result_signal)
        self.create_displayed_fig(fig)

    def push_to_seeq(self, *_):
        push_signal(self.result_signal, self.workbook_id, 'From My Add-on')

    def run(self):
        # noinspection PyTypeChecker
        # self.create_signals.on_event('click', self.push_to_seeq)
        return self
