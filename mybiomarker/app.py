import os
import dash
import base64
import gspread
import numpy as np

from dash import dcc, Dash, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash_bootstrap_components as dbc

from flask_login import current_user
from flask import Flask

from mybiomarker import db
from mybiomarker.models import User

from mybiomarker.data.transform_dataset import transform_blood_profile, transform_menstrual_data

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

df = transform_blood_profile()

df_menstrual_sorted = transform_menstrual_data()

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

    if profile == 'bone':
        return

    if profile == 'iron':
        return

    if profile == 'heart':
        return

    if profile == 'liver':
        return

    if profile == 'pancreatic':
        return

    if profile == 'female hormones':
        return

    if profile == 'eyes':
        return

    if profile == 'genetics':
        return

    if profile == 'gut':
        return

    if profile == 'cycle':
        return

    if profile == 'vitamins':
        return


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


fig_menstrual = go.Figure()

fig_menstrual.add_trace(
    go.Bar(
        y=df_menstrual_sorted['period_start'].to_list(),
        x=df_menstrual_sorted['period_length'].to_list(),
        name='period_length',
        hovertemplate='%{x} days',
        orientation='h',
        marker=dict(
            color="#eda4c0"
        )
    ),
)

fig_menstrual.add_trace(
    go.Bar(
        y=df_menstrual_sorted['period_start'].to_list(),
        x=df_menstrual_sorted['cycle_length'].to_list(),
        text=df_menstrual_sorted['cycle_length'],
        texttemplate="%{text} days",
        textposition='outside',
        name='cycle_length',
        orientation='h',
        hovertemplate='%{x} days',
        marker=dict(
            color='rgba(58, 71, 80, 0.6)',
        ),
    ),
)

fig_menstrual.update_layout(
    barmode='stack',
    plot_bgcolor='#f2f2f2',
    title='menstrual period and cycle length over the entire period'
)

period_start_date_range = df_menstrual_sorted['period_start'].to_list()
cycle_end_date_range = df_menstrual_sorted['cycle_end'].to_list()

fig_menstrual.update_layout(
    xaxis=dict(
        tick0=0,
        dtick=5, range=[0, 90]
    ),
)

fig_menstrual.update_yaxes(
    tickmode='array',
    tickvals=period_start_date_range,
)

fig_menstrual.update_layout(
    showlegend=False,
)

def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


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
            html.H2(f"🩸 1 day", className="card-title"),
            html.P("before menstruation starts", className="card-text"),
            html.P("last measured at: today", className="card-text"),

        ],
        body=True,
        color="dark",
        inverse=True,
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

menstrual_card_1 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("7 days", className="card-title"),
                html.P("Average period length", className="card-text"),
                html.Br(),
            ]
        ),
    ],
    color="dark",
    inverse=True,
)

menstrual_card_3 = dbc.Card(
    [
        html.Img(
            src=b64_image(image_filename),
            style={
                'height': '50%',
                'width': '50%'
            }
        ),
    ],
    style={'textAlign': 'center'},
    body=True,
    color="light",
)

menstrual_card_4 = dbc.Card(
    [
        dcc.Graph(
            id='graph1',
            figure=fig_menstrual,
        ),
    ],
    body=True,
    color="light",
)

menstrual_card_2 = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("70 days", className="card-title"),
                html.P("Average cycle length", className="card-text"),
                html.Br(),
            ]
        ),
    ],
    color="dark",
    inverse=True,
)

def init_dash_app(app):
    return Dash(__name__,
                external_stylesheets=[dbc.themes.MINTY],
                suppress_callback_exceptions=True,
                server=app,
                url_base_pathname='/hello-dashboard/',
                # routes_pathname_prefix="/dashboard/",
                )


def init_dash_layout(dash_app):
    # if current_user and current_user.is_authenticated:
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
    # return html.Div('403 Access Denied')


def init_dash_callbacks():
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
                html.H4('Menstrual cycle flow', style={"margin-top": 5}),
                html.Label('Everything you need to know about your cycle.'),
                dbc.Row([dbc.Col(menstrual_card_1), dbc.Col(menstrual_card_3), dbc.Col(menstrual_card_3),
                         dbc.Col(menstrual_card_2), ]),
                dbc.Row([dbc.Col(menstrual_card_4)]),

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


def serve_dash_app(app):
    dash_app = init_dash_app(app)
    # init_dash_callbacks()
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
                html.H4('Menstrual cycle flow', style={"margin-top": 5}),
                html.Label('Everything you need to know about your cycle.'),
                dbc.Row([dbc.Col(menstrual_card_1), dbc.Col(menstrual_card_3), dbc.Col(menstrual_card_3),
                         dbc.Col(menstrual_card_2), ]),
                dbc.Row([dbc.Col(menstrual_card_4)]),

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

    init_dash_layout(dash_app)

    return dash_app

import os
from flask import Flask

from flask_login import LoginManager, login_required


# init SQLAlchemy so we can use it later in our models


def protect_dashviews(dashapp):
    """If you want your Dash app to require a login,
    call this function with the Dash app you want to protect"""

    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(
                dashapp.server.view_functions[view_func]
            )

from flask_login import UserMixin


if __name__ == '__main__':

    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') or 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user.
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from mybiomarker.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from mybiomarker.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from mybiomarker import models

    with app.app_context():
        db.create_all()

    dash_app = serve_dash_app(app)

    dash_app.run()
