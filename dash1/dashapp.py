from _app.dash import DashWrapper
from .layout import layout
from .callbacks import register_callbacks


__all__ = [
    "DashApp1",
]


class DashApp1(DashWrapper):
    key = "dash_app_1"
    title = "Dash App 1"
    layout = layout
    register_callbacks = register_callbacks
