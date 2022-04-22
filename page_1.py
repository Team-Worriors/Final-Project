import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from interactive_trader import *
from datetime import datetime
from ibapi.contract import Contract
from ibapi.order import Order
import time
import threading
import pandas as pd

df = pd.DataFrame(
    columns=['date', 'ticker', 'price', 'quantity', 'action', 'trip',
             'status']
)

page_1 = html.Div(
    children=[
        # Section title
        html.H1("Backtesing"),

        html.Br(),
        html.P("Pairs Trading is a trading strategy which involves finding "
               "a pair of stocks that exhibit similar historical price behavior, "
               "and then betting on the subsequent convergence of their prices "
               "in the event that they diverge."),

        html.Br(),
        html.P("Z-score is the normalized price ratio of the pairs. "
               "In this case, the ratio of the pairs is "
               "ko’s close price / pep’s close price. "
               "It is computed using moving averages at each given time "
               "and tells us whether it's a good idea to enter a position "
               "at this time. When the Z-score goes above the short threshold, λ, "
               "we sell ko and buy pep. When the Z-score goes below the long "
               "threshold, -λ, we buy ko and sell pep."),

        html.Br(),
        html.P("ρ sets exit threshold level (should be less than λ). "
               "Limit order will be filled at either entry price*(1+ρ) or entry price*(1-ρ)."),

        html.Br(),
        html.P(["Column ‘status’ will show: ", html.Br(),
                "- ‘FILLED’ if the limit order filled, ", html.Br(),
                "- ‘TIMEOUT’ if the order stayed open for X days, ", html.Br(),
                "- ‘OPEN’ if the order stayed open for less than X days, ", html.Br(),
                "- ‘STOPLOSS’ if the value dipped below your tolerance set by L."]),
        html.Br(),

        # parameter n
        html.Br(),
        html.H5("Enter the value for rolling window:"),
        html.Div(
            children=[
                dcc.Input(id='n-rolling', type='number', value=60, step=1, debounce=True)
            ],
            style={
                'display': 'inline-block',
                'margin-right': '20px',
            }
        ),
        html.Br(),

        # parameter Lamda
        html.Br(),
        html.H5("Enter the value for entry signal Lambda:"),
        html.Div(
            children=[
                dcc.Input(id='Lambda', type='number', value=1, debounce=True)
            ],
            style={
                'display': 'inline-block',
                'margin-right': '20px',
            }
        ),
        html.Br(),

        # parameter Rho
        html.Br(),
        html.H5("Enter the value for exit signal Rho:"),
        html.Div(
            children=[
                dcc.Input(id='rho', type='number', value=0.02, debounce=True)
            ],
            style={
                'display': 'inline-block',
                'margin-right': '20px',
            }
        ),
        html.Br(),

        # parameter L
        html.Br(),
        html.H5("Enter the value for loss limit L (%):"),
        html.Div(
            children=[
                dcc.Input(id='loss-limit', type='number', value=20, debounce=True)
            ],
            style={
                'display': 'inline-block',
                'margin-right': '20px',
            }
        ),
        html.Br(),

        # parameter X
        html.Br(),
        html.H5("Enter the value for order open days X:"),
        html.Div(
            children=[
                dcc.Input(id='open-days', type='number', value=60, debounce=True)
            ],
            style={
                'display': 'inline-block',
                'margin-right': '20px',
            }
        ),
        html.Br(),

        html.Br(),
        html.H5("Press run to start backtesting:"),
        # Run button
        html.Button('Run', id='run-button', n_clicks=0),
        html.Br(),

        html.Br(),
        html.Br(),
        html.H4("Ledger:"),
        html.Div(
            dcc.Loading(
                id="loading-1",
                type="default",
                children=dash_table.DataTable(
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    id='backtest-dt'
                )
            )
        ),
    ],
    id="page-1"
)
