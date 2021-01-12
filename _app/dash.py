from pathlib import Path
from typing import Callable

from dash import Dash
from dash.development.base_component import Component
from flask import Flask
from jinja2.filters import do_mark_safe


class EmbeddedDash(Dash):
    def __init__(self, *args, **kwargs):
        self.index_string_inline = kwargs.pop("inline_index_string")
        super().__init__(*args, **kwargs)
        self.index_string_regular = self.index_string

    def index(self, *args, **kwargs):
        is_inline = kwargs.pop("inline", False)

        # TODO is this thread-safe? Probably not
        if is_inline:
            self.index_string = self.index_string_inline
        else:
            self.index_string = self.index_string_regular
        return super().index(*args, **kwargs)


class DashWrapper:
    key: str
    layout: Component
    register_callbacks: Callable
    title: str
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no",
    }
    _registered = False

    @classmethod
    def register(cls, app: Flask):
        if cls._registered:
            raise ValueError(f"{cls} has already been registered.")
        cls._registered = True
        dashapp = EmbeddedDash(
            __name__,
            server=app,
            url_base_pathname=f"/{cls.key}/",
            assets_folder=Path(__file__).parent / "assets",
            meta_tags=[cls.meta_viewport],
            inline_index_string=f"""
                <div id="{cls.key}">
                    {{%app_entry%}}
                    <footer>
                        {{%config%}}
                        {{%scripts%}}
                        {{%renderer%}}
                    </footer>
                </div>
            """
        )

        with app.app_context():
            dashapp.title = cls.title
            dashapp.layout = cls.layout
            cls.register_callbacks(dashapp)

        @app.context_processor
        def add_to_template_context():
            return {cls.key: lambda: do_mark_safe(dashapp.index(inline=True))}
