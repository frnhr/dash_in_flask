import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import aerosandbox as asb
import casadi as cas
from .airplane import make_airplane
import numpy as np
import pandas as pd


def register_callbacks(dashapp):
    app = dashapp

    def make_table(dataframe):
        return dbc.Table.from_dataframe(
            dataframe, bordered=True, hover=True, responsive=True,
            striped=True, style={}
        )

    @app.callback(
        [Output("display", "figure"), Output("output", "children")],
        [
            Input("display_geometry", "n_clicks_timestamp"),
            Input("run_ll_analysis", "n_clicks_timestamp"),
            Input("run_vlm_analysis", "n_clicks_timestamp"),
        ],
        [State("n_booms", "value"), State("wing_span", "value"),
         State("alpha", "value"), ],
    )
    def display_geometry(
            display_geometry, run_ll_analysis, run_vlm_analysis, n_booms,
            wing_span, alpha,
    ):
        ### Figure out which button was clicked
        try:
            button_pressed = np.argmax(
                np.array(
                    [
                        float(display_geometry),
                        float(run_ll_analysis),
                        float(run_vlm_analysis),
                    ]
                )
            )
            assert button_pressed is not None
        except:
            button_pressed = 0

        ### Make the airplane
        airplane = make_airplane(n_booms=n_booms, wing_span=wing_span, )
        op_point = asb.OperatingPoint(density=0.10, velocity=20, alpha=alpha, )
        if button_pressed == 0:
            # Display the geometry
            figure = airplane.draw(show=False, colorbar_title=None)
            output = "Please run an analysis to display the data."
        elif button_pressed == 1:
            # Run an analysis
            opti = cas.Opti()  # Initialize an analysis/optimization environment
            ap = asb.Casll1(
                airplane=airplane, op_point=op_point, opti=opti,
                run_setup=False
            )
            ap.setup(verbose=False)
            # Solver options
            p_opts = {}
            s_opts = {}
            # s_opts["mu_strategy"] = "adaptive"
            opti.solver("ipopt", p_opts, s_opts)
            # Solve
            try:
                sol = opti.solve()
            except RuntimeError:
                sol = opti.debug
                raise Exception("An error occurred!")

            figure = ap.draw(show=False)  # Generates figure

            output = make_table(
                pd.DataFrame(
                    {
                        "Figure": ["CL", "CD", "CDi", "CDp", "L/D"],
                        "Value": [
                            sol.value(ap.CL),
                            sol.value(ap.CD),
                            sol.value(ap.CDi),
                            sol.value(ap.CDp),
                            sol.value(ap.CL / ap.CD),
                        ],
                    }
                )
            )

        elif button_pressed == 2:
            # Run an analysis
            opti = cas.Opti()  # Initialize an analysis/optimization environment
            ap = asb.Casvlm1(
                airplane=airplane, op_point=op_point, opti=opti,
                run_setup=False
            )
            ap.setup(verbose=False)
            # Solver options
            p_opts = {}
            s_opts = {}
            # s_opts["mu_strategy"] = "adaptive"
            opti.solver("ipopt", p_opts, s_opts)
            # Solve
            try:
                sol = opti.solve()
            except RuntimeError:
                sol = opti.debug
                raise Exception("An error occurred!")

            figure = ap.draw(show=False)  # Generates figure

            output = make_table(
                pd.DataFrame(
                    {
                        "Figure": ["CL", "CDi", "L/Di"],
                        "Value": [
                            sol.value(ap.CL),
                            sol.value(ap.CDi),
                            sol.value(ap.CL / ap.CDi),
                        ],
                    }
                )
            )

        figure.update_layout(
            autosize=True,
            # width=1000,
            # height=700,
            margin=dict(l=0, r=0, b=0, t=0, ),
        )

        return (figure, output)
