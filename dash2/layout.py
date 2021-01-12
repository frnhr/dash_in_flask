import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Solar Aircraft Design with AeroSandbox and Dash"),
                        html.H5("Peter Sharpe"),
                    ],
                    width=True,
                ),
                # dbc.Col([
                #     html.Img(src="assets/MIT-logo-red-gray-72x38.svg", alt="MIT Logo", height="30px"),
                # ], width=1)
            ],
            align="end",
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H5("Key Parameters"),
                                html.P("Number of booms:"),
                                dcc.Slider(
                                    id="n_booms",
                                    min=1,
                                    max=3,
                                    step=1,
                                    value=3,
                                    marks={1: "1", 2: "2", 3: "3",},
                                ),
                                html.P("Wing Span [m]:"),
                                dcc.Input(id="wing_span", value=43, type="number"),
                                html.P("Angle of Attack [deg]:"),
                                dcc.Input(id="alpha", value=7.0, type="number"),
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.H5("Commands"),
                                dbc.Button(
                                    "Display (1s)",
                                    id="display_geometry",
                                    color="primary",
                                    style={"margin": "5px"},
                                    n_clicks_timestamp="0",
                                ),
                                dbc.Button(
                                    "LL Analysis (3s)",
                                    id="run_ll_analysis",
                                    color="secondary",
                                    style={"margin": "5px"},
                                    n_clicks_timestamp="0",
                                ),
                                dbc.Button(
                                    "VLM Analysis (15s)",
                                    id="run_vlm_analysis",
                                    color="secondary",
                                    style={"margin": "5px"},
                                    n_clicks_timestamp="0",
                                ),
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.H5("Aerodynamic Performance"),
                                dbc.Spinner(html.P(id="output"), color="primary",),
                            ]
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        # html.Div(id='display')
                        dbc.Spinner(
                            dcc.Graph(id="display", style={"height": "80vh"}),
                            color="primary",
                        )
                    ],
                    width=True,
                ),
            ]
        ),
        html.Hr(),
        html.P(
            [
                html.A(
                    "Source code",
                    href="https://github.com/peterdsharpe/AeroSandbox-Interactive-Demo",
                ),
                ". Aircraft design tools powered by ",
                html.A(
                    "AeroSandbox", href="https://peterdsharpe.github.com/AeroSandbox"
                ),
                ". Build beautiful UIs for your scientific computing apps with ",
                html.A("Plot.ly ", href="https://plotly.com/"),
                "and ",
                html.A("Dash", href="https://plotly.com/dash/"),
                "!",
            ]
        ),
    ],
    fluid=True,
)