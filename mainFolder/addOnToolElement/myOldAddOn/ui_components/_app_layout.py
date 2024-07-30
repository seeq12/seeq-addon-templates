import ipyvuetify as v
import traitlets
from typing import Callable
import ipywidgets as widgets
from pathlib import Path

from ._hamburger_menu import HamburgerMenu

CURRENT_DIR = Path(__file__).parent.resolve()
TEMPLATES_DIR = CURRENT_DIR.joinpath('templates')
STATIC_DIR = TEMPLATES_DIR.joinpath('static')
TEMPLATE_FILE = '_app_layout.vue'


class AppLayout(v.VuetifyTemplate):
    """
    UI component - Layout of the Add-on

    Attributes
    ----------
    btn_loading: bool
        If True, it shows the loading spinner on the Signal to Workbench button
    btn_disabled: bool
        If True, it disables the Signal to Workbench button
    disabled_controls: bool
        If True, it disables all components within the v-card
    first_dropdown_items: list
        Items of the First Signal dropdown
    first_dropdown_value: str
        Selected item of the First Signal dropdown
    math_operator_value: str
        Selected item of the Math Operator dropdown
    second_dropdown_items: list
        Items of the Second Signal dropdown
    second_dropdown_value: str
        Selected item of the Second Signal dropdown
    signal_plot: plotly.graph_objects.FigureWidget
        A plotly.graph_objects.FigureWidget instance with the Plotly plot of
        the resulting signal.
    visualization: {'plot', 'message'}
        If 'plot', it will display the AppLayout.signal_plot widget;
        if 'message', it will display the alternative message instead of the plot.
    template_file: str
        Modifies the VueTemplate.template_file attribute with the
        ui_components.templates._app_layout.vue template
    """

    template_file = str(TEMPLATES_DIR.joinpath(TEMPLATE_FILE))

    disabled_controls = traitlets.Bool(default_value=False).tag(sync=True)
    btn_disabled = traitlets.Bool(default_value=True).tag(sync=True)
    first_dropdown_items = traitlets.List(default_value=[]).tag(sync=True)
    first_dropdown_value = traitlets.Unicode(default_value='').tag(sync=True)
    math_operator_value = traitlets.Unicode(default_value='+').tag(sync=True)
    second_dropdown_items = traitlets.List(default_value=[]).tag(sync=True)
    second_dropdown_value = traitlets.Unicode(default_value='').tag(sync=True)
    btn_loading = traitlets.Bool(default_value=False).tag(sync=True)
    signal_plot = traitlets.Any().tag(sync=True, **widgets.widget_serialization)
    visualization = traitlets.Unicode(default_value='message').tag(sync=True)

    def __init__(self,
                 *args,
                 first_signal_on_change: Callable[[str], None] = None,
                 second_signal_on_change: Callable[[str], None] = None,
                 math_operator_on_change: Callable[[str], None] = None,
                 push_to_seeq_on_click: Callable[[], None] = None,
                 **kwargs
                 ):
        super().__init__(*args, **kwargs)

        # Components
        self.hamburger_menu = HamburgerMenu(**kwargs)

        self.components = {
            'hamburger-menu': self.hamburger_menu,
        }

        # user callback functions
        self.first_signal_on_change = first_signal_on_change
        self.second_signal_on_change = second_signal_on_change
        self.math_operator_on_change = math_operator_on_change
        self.push_to_seeq_on_click = push_to_seeq_on_click

    def vue_first_signal_on_change(self, data):
        if self.first_signal_on_change is not None:
            self.first_signal_on_change(data)

    def vue_second_signal_on_change(self, data):
        if self.second_signal_on_change is not None:
            self.second_signal_on_change(data)

    def vue_math_operator_on_change(self, data):
        if self.math_operator_on_change is not None:
            self.math_operator_on_change(data)

    def vue_push_to_seeq_on_click(self, data):
        if self.push_to_seeq_on_click is not None:
            self.push_to_seeq_on_click(data)
