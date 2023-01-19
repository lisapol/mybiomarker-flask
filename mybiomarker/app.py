# basic import
import os
import dash
import base64
import gspread

# dash libraries
from dash import dcc, Dash, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# visualisations
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# flask
from flask_login import LoginManager, login_required
from flask import Flask, render_template, request, flash, redirect, url_for

# mybiomarker
from mybiomarker import db
from mybiomarker.models import User
from mybiomarker.auth import auth as auth_blueprint
from mybiomarker.main import main as main_blueprint
from mybiomarker.data.transform_dataset import transform_blood_profile, transform_menstrual_data


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') or 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

df = transform_blood_profile()

dir_path = os.path.dirname(os.path.realpath(__file__))
image_filename = f'{dir_path}/dash_app/girl.png'

color_dict = {
    'low': 'yellow',
    'optimal': 'yellow',
    'near-optimal': 'yellow',
    'desirable': 'green',
    'normal': 'green',
    'borderline-high': 'red',
    'high': 'red',
    'very high': 'red'
}


def _find_profile(profile: str) -> list:
    if profile == 'lipid':
        return ['cholesterol total', 'HDL cholesterol', 'LDL cholesterol', 'triglycerides']

    if profile == 'thyroid':
        return ['TSH', 'FT4', 'T4', 'FT3', 'T3', 'TgAb', 'TPOAb', 'Tg']

    if profile == 'full blood count':
        return

    if profile == 'inflammation':
        return ['C-reactive protein']



def plot_test(df, profile, dt='all'):
    name = _find_profile(profile)
    if not name:
        return f"no data for {profile} profile"

    fig = go.Figure()

    if dt != 'all':
        df = df[df['test_dt'] == dt]

    for number, test_name in enumerate(name):
        #         df_test = df[df["test_name_eng"] == test_name]
        df_test = df[df["test_name_eng"] == test_name]
        #         print(df_test)

        # skip ploting null values
        if df_test.shape[0] > 0:
            #                 print(df_test['test_dt'], df_test['test_name_eng'], df_test['test_results'])
            fig.add_trace(
                go.Bar(
                    x=df_test['test_dt'].astype(str),
                    y=df_test['test_results'].astype(float),
                    name=test_name,
                    hovertemplate=df_test['test_results'],
                    marker_color=px.colors.sequential.Burg[number - 1]
                )
            )

    fig.update_layout(barmode='group',
                      xaxis_tickangle=45,  # -45
                      title=f'{profile} profile',
                      xaxis={'type': 'category', 'categoryorder': 'category ascending'},
                      xaxis_title="dt",
                      yaxis_title="test results",
                      plot_bgcolor='#f2f2f2',
                      showlegend=False,
                      )

    return fig


def show_all_dt_for_the_profile(profile: str) -> list:
    df_profile = df[df['test_name_eng'].isin(_find_profile(profile))].test_dt.unique()
    df_profile = np.append(df_profile, 'all')
    return df_profile


def Header(name, app):
    title = html.H2(name, style={"margin-top": 5})
    return dbc.Row([dbc.Col(title, md=9)])


def LabeledSelect(label, **kwargs):
    return dbc.Form([dbc.Label(label), dbc.Select(**kwargs)])


popover_children = "I am a popover!"

# Card components
cards = [
    dbc.Card(
        [
            html.H2(f"❤️ 140/90", className="card-title"),
            html.P("body pressure", className="card-text"),
            html.P("last measured at: today", className="card-text"),
        ],
        body=True,
        color="light",
    ),
    dbc.Card(
        [
            html.H2(f"177 cm", className="card-title"),
            html.P("height", className="card-text"),
            html.P("last measured at: today", className="card-text"),

        ],
        body=True,
        color="primary",
        inverse=True,
    ),
    dbc.Card(
        [
            html.H2("62 kg", className="card-title"),
            html.P("weight", className="card-text"),
            html.P("last measured at: today", className="card-text"),
        ],
        body=True,
        color="primary",
        inverse=True,
    ),
]


keys = ['lipid', 'thyroid', 'inflammation']


graphs = dbc.Row(
    [
        dbc.Col(
            [
                LabeledSelect(
                    id="year-filter",
                    options=[{"label": Year, "value": Year} for Year in keys],
                    value='lipid',
                    label="choose organ to explore:",
                ),
            ],
            width=6,
        ),
        dbc.Col(
            [
                LabeledSelect(
                    id="dt-filter",
                    value='all',
                    label="choose time to explore:",
                ),
            ],
            width=6,
        ),
        dcc.Graph(id="bar"),
    ],
)

hh = [
    dbc.Button("explain my results",
               id="legacy-target",
               color="primary",
               n_clicks=0
               ),
    dbc.Popover(
        popover_children,
        target="legacy-target",
        body=True,
        trigger="legacy",
    )
]


dash_app = Dash(__name__,
                external_stylesheets=[dbc.themes.MINTY],
                suppress_callback_exceptions=True,
                server=app,
                # routes_pathname_prefix="/dashboard/",
                url_base_pathname="/hello-dashboard/"
                )
dash_app.layout = dbc.Container(
    [
        Header("Welcome back 👋", dash_app),
        html.Hr(),
        dbc.Tabs(
            [
                dbc.Tab(label="me", tab_id="scatter"),
                dbc.Tab(label="mom", tab_id="histogram"),
            ],
            id="tabs",
            active_tab="scatter",
        ),
        html.Div(id="tab-content", className="p-4"),
    ],
    fluid=False,
)


@dash_app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab == "scatter":
        return [
            dbc.Row([dbc.Col(card) for card in cards]),
            html.Br(),
            html.Hr(),
            html.H4('Medical analysis overview', style={"margin-top": 5}),
            html.Hr(),
            dbc.Row([dbc.Col(graph) for graph in hh]),
            html.Br(),
            graphs,
        ]
    elif active_tab == "histogram":
        return None


@dash_app.callback(
    Output("bar", "figure"),
    [Input("year-filter", "value"), Input("dt-filter", "value")],
)
def update_charts(Year, dt):
    fig = plot_test(df, profile=Year, dt=dt)
    return fig


@dash_app.callback(
    dash.dependencies.Output('dt-filter', 'options'),
    [dash.dependencies.Input('year-filter', 'value')]
)
def update_date_dropdown(name):
    opts = show_all_dt_for_the_profile(name)
    options = [{'label': opt, 'value': opt} for opt in opts]
    return options

@app.route('/')
def index():
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user.
    return User.query.get(int(user_id))


# registering blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)


if __name__ == '__main__':
    app.debug = True
    # blueprint for auth routes in our app
    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(
                dash_app.server.view_functions[view_function])

    dash_app.run()
