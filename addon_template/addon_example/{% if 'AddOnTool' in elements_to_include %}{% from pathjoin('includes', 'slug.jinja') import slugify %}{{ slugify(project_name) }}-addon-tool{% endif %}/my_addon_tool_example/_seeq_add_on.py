import warnings
import pandas as pd
from IPython.display import clear_output

from . import create_new_signal, create_matplotlib_widget, pull_only_signals, AppLayout
from ._backend import push_signal
from .utils import get_workbook_worksheet_workstep_ids, get_worksheet_url

warnings.filterwarnings('ignore')


class MyAddonToolExample(AppLayout):
    """
    This is the main class for the User Interface of the <Add on Name> Add-on.
    To create an instance, either a Seeq Data Lab project URL with appropriate
    query parameters or pd.DataFrame must be passed.

    """

    def __init__(self, sdl_notebook_url):
        self.workbook_id, self.worksheet_id, self.workstep_id = get_workbook_worksheet_workstep_ids(
            sdl_notebook_url)
        self.worksheet_url = get_worksheet_url(sdl_notebook_url)
        self.df = pull_only_signals(self.worksheet_url)
        self.result_signal = pd.DataFrame()
        clear_output()

        super(MyAddonToolExample, self).__init__(
            first_signal_on_change=self.first_signal_dropdown,
            second_signal_on_change=self.second_signal_dropdown,
            math_operator_on_change=self.math_operator_dropdown,
            push_to_seeq_on_click=self.push_to_seeq
        )

        self.first_signal.items = list(self.df.columns)
        self.second_signal.items = list(self.df.columns)
        self.create_displayed_fig()

    def math_operation(self):
        if self.math_operator.v_model == '+':
            return 'add'
        if self.math_operator.v_model == '-':
            return 'subtract'
        if self.math_operator.v_model == 'x':
            return 'multiply'
        if self.math_operator.v_model == '/':
            return 'divide'

    def first_signal_dropdown(self, widget, event, data):
        # ipyvuetify doesn't assign the value of the component till the end of the callback. Thus, assigned manually
        self.first_signal.v_model = data
        self.update_display()

    def second_signal_dropdown(self, widget, event, data):
        # ipyvuetify doesn't assign the value of the component till the end of the callback. Thus, assigned manually
        self.second_signal.v_model = data
        self.update_display()

    def math_operator_dropdown(self, widget, event, data):
        # ipyvuetify doesn't assign the value of the component till the end of the callback. Thus, assigned manually
        self.math_operator.v_model = data
        self.update_display()

    def show_ui_component(self, component):
        hide_object = 'display: none !important;'
        self.matplotlib_plot.style_ = hide_object
        self.spinner.style_ = hide_object
        self.message.style_ = hide_object
        if component == 'message':
            self.message.style_ = ''
        if component == 'plot':
            self.matplotlib_plot.style_ = ''
        if component == 'spinner':
            self.spinner.style_ = 'height: 200px;'

    def create_displayed_fig(self):
        self.controls.disabled = False
        if self.result_signal.empty:
            self.show_ui_component('message')
            return

        self.save_button.disabled = False
        self.matplotlib_plot.children = [create_matplotlib_widget(self.result_signal)]
        self.show_ui_component('plot')

    def update_display(self, *_):
        print('display here')
        self.result_signal = pd.DataFrame()
        self.controls.disabled = True
        self.show_ui_component('spinner')
        self.save_button.disabled = True
        if {self.first_signal.v_model, self.second_signal.v_model}.issubset(set(self.df.columns)):
            print("here")
            self.result_signal = create_new_signal(self.df[self.first_signal.v_model].values,
                                                   self.df[self.second_signal.v_model].values,
                                                   self.df.index,
                                                   self.math_operation())

        self.create_displayed_fig()

    def push_to_seeq(self, *_):
        push_signal(self.result_signal, self.workbook_id, self.worksheet_id)

    def run(self):
        return self.app
