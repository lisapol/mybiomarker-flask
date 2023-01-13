from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

import gspread
import base64

import plotly.graph_objects as go

from oauth2client.service_account import ServiceAccountCredentials

import dash
import dash_bootstrap_components as dbc

from dash import dcc, Dash
from dash import html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import flask
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv (f'{dir_path}/dash_1/my_data.csv')


df = df[
    ["id","test_dt","test_name_eng","test_results","test_norm_min","test_norm_max","test_unit_eng"]
]

##Convert number strings to floats
df = df.apply(pd.to_numeric, errors='ignore')
df['test_dt'] = pd.to_datetime(df['test_dt']).dt.strftime('%Y-%m-%d')
# drop duplicates and keep row with max values
df = df.sort_values('test_results', ascending=False)


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
                      xaxis_tickangle=0,  # -45
                      title=f'{profile} profile',
                      xaxis={'type': 'category', 'categoryorder': 'category ascending'},
                      xaxis_title="dt",
                      yaxis_title="test results",
                      plot_bgcolor='#f2f2f2'
                      )

    return fig

import numpy as np


def show_all_dt_for_the_profile(profile: str) -> list:
    df_profile = df[df['test_name_eng'].isin(_find_profile(profile))].test_dt.unique()
    df_profile = np.append(df_profile, 'all')
    return df_profile


df_menstrual = pd.DataFrame(columns=[
    'id',
    'period_start',
    'period_end',
]
)

df_menstrual = df_menstrual.append(
    {'id': 4,
     'period_start': '2022-08-09',
     'period_end': '2022-08-14',
     },
    ignore_index=True
)
df_menstrual = df_menstrual.append(
    {'id': 5,
     'period_start': '2022-10-20',
     'period_end': '2022-10-25',
     },
    ignore_index=True
)

df_menstrual = df_menstrual.append(
    {'id': 6,
     'period_start': '2023-01-05',
     'period_end': '',
     },
    ignore_index=True
)

df_menstrual = df_menstrual.append(
    {'id': 7,
     'period_start': '2021-01-16',
     'period_end': '2021-01-20',
     },
    ignore_index=True
)

df_menstrual = df_menstrual.append(
    {'id': 8,
     'period_start': '2021-02-19',
     'period_end': '2021-02-24',
     },
    ignore_index=True
)

df_menstrual = df_menstrual.append(
    {'id': 9,
     'period_start': '2021-03-27',
     'period_end': '2021-04-01',
     },
    ignore_index=True
)

df_menstrual = df_menstrual.append(
    {'id': 10,
     'period_start': '2021-05-04',
     'period_end': '2021-05-09',
     },
    ignore_index=True
)

df_menstrual = df_menstrual.append(
    {'id': 11,
     'period_start': '2021-06-07',
     'period_end': '2021-06-12',
     },
    ignore_index=True
)


df_menstrual['period_end'] = pd.to_datetime(df_menstrual['period_end'])
df_menstrual['period_start'] = pd.to_datetime(df_menstrual['period_start'])

df_menstrual['period_length'] = (df_menstrual['period_end'] - df_menstrual['period_start']) + pd.Timedelta(days=1)

df_menstrual_sorted = df_menstrual.sort_values(by=['period_start', 'period_end'], ascending=True)

df_menstrual_sorted['cycle_end'] = df_menstrual_sorted.period_start.shift(-1) - pd.Timedelta(days=1)

df_menstrual_sorted['cycle_end'] = pd.to_datetime(df_menstrual_sorted['cycle_end'])

df_menstrual_sorted['cycle_length'] = (df_menstrual_sorted['cycle_end'] - df_menstrual_sorted[
    'period_start']) + pd.Timedelta(days=1)

df_menstrual_sorted['period_length'] = df_menstrual_sorted['period_length'].dt.days

df_menstrual_sorted['cycle_length'] = df_menstrual_sorted['cycle_length'].dt.days

df_menstrual_sorted = df_menstrual_sorted.dropna()


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
    #     secondary_y=True
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
    #     secondary_y=False,
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
    #     secondary_y=False,
    #     side='left',
    #     tickformat='%Y-%m-%d',
    tickmode='array',
    tickvals=period_start_date_range,
)



fig_menstrual.update_layout(
    showlegend=False,
)


image_filename = f'{dir_path}/dash_1/girl.png'


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
                    #             options=[{"label": opt, "value": opt} for opt in keys],
                    #             value='2023-01-01',
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
    #     style={"width": "18rem"},
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
        #         dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                html.H4("70 days", className="card-title"),
                html.P("Average cycle length", className="card-text"),
                html.Br(),
            ]
        ),
        #         dbc.CardFooter("This is the footer"),
    ],
    #     style={"width": "18rem"},
    color="dark",
    inverse=True,
)

dash_app = Dash(__name__,
                external_stylesheets=[dbc.themes.MINTY],
                suppress_callback_exceptions=True,
                server=app,
                routes_pathname_prefix="/dash_1/",
                )
dash_app.layout = dbc.Container(
    #     dcc.Store(id="store"),
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

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    dash_app.run()
