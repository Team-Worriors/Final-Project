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
        html.H1("Section 1: Backtesing"),

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

        html.H5("Press run to start backtesting:"),
        # Run button
        html.Button('Run', id='run-button', n_clicks=0),
        html.Br(),

        html.Br(),
        html.Br(),
        html.H4("Ledger:"),
        dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            id='backtest-dt'
        )
    ],
    id="page-1"
)
