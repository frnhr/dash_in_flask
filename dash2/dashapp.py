from _app.dash import DashWrapper
from .layout import layout
from .callbacks import register_callbacks


__all__ = [
    "DashApp2",
]


class DashApp2(DashWrapper):
    key = "dash_app_2"
    title = "Dash App 2"
    layout = layout
    register_callbacks = register_callbacks
