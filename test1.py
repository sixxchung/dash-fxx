import os
import pandas as pd
import numpy as np


from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

#import plotly.express as px
import plotly.graph_objects as go
#from plotly.graph import DEFAULT_PLOTLY_COLORS
from plotly.colors import DEFAULT_PLOTLY_COLORS 

url_salesData = 'https://raw.githubusercontent.com/sixxchung/pythondash/6236fbca647de6562c5685de724a08362bd1afea/data/Sales%20data/Data.csv'
df_o = pd.read_csv(url_salesData)
df = df_o.copy()

df['year']=df['OrderDate'].str.slice(0,4)
df['month']=df['OrderDate'].str.slice(5,7)
df = df.sort_values(by=['Region', 'Channel', 'Category', 'Item Type', 'year', 'month', 'Gender' ])
# df.info()
years = list(df['year'].unique())
years.sort()
# d20 = df[ df.year=='2020'].copy()
# d20['Margin'] = d20['Revenue'] - d20['Cost']

dash_app = Dash(
    name = __name__,
    #server = server,
)
#server = dash_app.server

dash_app.title = ('Dashboard - Sales data')
dash_app.layout = html.Div(children=[
    html.H2('Sales Dashboard with Dash', style={'textAlign':'center'}),

    html.Div(style={'background-color':'red'}, children=[html.Div(dcc.Graph(id='channel1'))]),
    html.Div(style={'background-color':'blue'}, children=[html.Div(dcc.Graph(id='channel2'))]),

    html.Div(className='Left', children=[
        html.Div(className='Pie',
            children=[
                html.Div(dcc.Graph(id='channel'),  style={'float':'left',  'display':'inline-block', 'width':'33%'}),
                html.Div(dcc.Graph(id='gender'),   style={'float':'left',  'display':'inline-block', 'width':'33%'}),
                html.Div(dcc.Graph(id='agegroup'), style={'float':'right',                           'width':'33%'}), 
            ]
        ),
        html.Div(className='Indicator & bar',
            children=[
                html.Div(dcc.Graph(id='idc_africa'),  style={'float':'left', 'display':'inline-block', 'width':'12%'}),
                html.Div(dcc.Graph(id='idc_america'), style={'float':'left', 'display':'inline-block', 'width':'12%'}),
                html.Div(dcc.Graph(id='idc_asia'),    style={'float':'left', 'display':'inline-block', 'width':'12%'}),
                html.Div(dcc.Graph(id='idc_europe'),  style={'float':'left', 'display':'inline-block', 'width':'12%'}),
                html.Div(dcc.Graph(id='idc_oceania'), style={'float':'left', 'display':'inline-block', 'width':'12%'}),
                html.Div(dcc.Graph(id='country'),     style={'float':'right',                          'width':'40%'}),
            ]
        ),
        html.Div(className='Line', style={'float':'left', 'display':'inline-block', 'width':'65%'},
            children=[
                html.Div(dcc.Graph(id='line'),  style={'float':'left', 'display':'inline-block', 'width':'60%'}),
                html.Div(dcc.Graph(id='radar'), style={'float':'right',                          'width':'40%'}),
            ]
        ),
    ]),

    html.Div([ #className='Right', children=[
        html.Div(#className='rightdown', #style={'float':'right', 'width':'35%'},
            children=[
                html.Div(dcc.Dropdown(id = 'id_year',
                    options=[{'label':i, 'value':i} for i in years],
                    value = max(years),
                    style={'width':'50%'})),
                html.Div(dcc.Graph(id='map')),
                html.Div(dcc.Graph(id='sankey')),
            ]
        ),        
    ])
])

cols = DEFAULT_PLOTLY_COLORS

@dash_app.callback(
    [Output('channel',  'figure'),
     Output('gender',   'figure'),
     Output('agegroup', 'figure')],
    [Input('id_year', 'value')]) 
def update_output(val):
    pies = ['Channel', 'Gender', 'AgeGroup']
    figures = []
    return None

if __name__=='__main__':
    dash_app.run_server(debug=False)


