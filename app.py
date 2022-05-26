import os
import pandas as pd
import numpy as np

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

#import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import DEFAULT_PLOTLY_COLORS

url_salesData = 'https://raw.githubusercontent.com/sixxchung/pythondash/6236fbca647de6562c5685de724a08362bd1afea/data/Sales%20data/Data.csv'
df_o = pd.read_csv(url_salesData)
df = df_o.copy()

df['year'] = df['OrderDate'].str.slice(0, 4)
df['month'] = df['OrderDate'].str.slice(5, 7)
df['Margin'] = df['Revenue'] - df['Cost']
df = df.sort_values(by=['Region', 'Channel', 'Category',
                    'Item Type', 'year', 'month', 'Gender'])
# df.info()
years = list(df['year'].unique())
years.sort()
# d20 = df[ df.year=='2020'].copy()
# d20['Margin'] = d20['Revenue'] - d20['Cost']

dash_app = Dash(
    name=__name__,
    #server = server,
)
#server = dash_app.server

dash_app.title = ('Dashboard - Sales data')
dash_app.layout = html.Div(children=[
    html.H2('Sales Dashboard with Dash', style={'textAlign': 'center'}),
    # 영역나누기
    html.Div(className='LeftPad', style={'float': 'left', 'display': 'inline-block', 'width': '65%'}, children=[
        html.Div(className='Pie',
                 children=[
                     html.Div(dcc.Graph(id='channel'),  style={
                              'float': 'left',  'display': 'inline-block', 'width': '33%'}),
                     html.Div(dcc.Graph(id='gender'),   style={
                              'float': 'left',  'display': 'inline-block', 'width': '33%'}),
                     html.Div(dcc.Graph(id='agegroup'), style={
                              'float': 'right',                           'width': '33%'}),
                 ]
                 ),
        html.Div(className='Indicator & bar',
                 children=[
                     html.Div(dcc.Graph(id='idc_africa'),  style={
                              'float': 'left', 'display': 'inline-block', 'width': '12%'}),
                     html.Div(dcc.Graph(id='idc_america'), style={
                              'float': 'left', 'display': 'inline-block', 'width': '12%'}),
                     html.Div(dcc.Graph(id='idc_asia'),    style={
                              'float': 'left', 'display': 'inline-block', 'width': '12%'}),
                     html.Div(dcc.Graph(id='idc_europe'),  style={
                              'float': 'left', 'display': 'inline-block', 'width': '12%'}),
                     html.Div(dcc.Graph(id='idc_oceania'), style={
                              'float': 'left', 'display': 'inline-block', 'width': '12%'}),
                     html.Div(dcc.Graph(id='country'),     style={
                              'float': 'right',                          'width': '40%'}),
                 ]
                 ),
        html.Div(className='Line',
                 children=[
                     html.Div(dcc.Graph(id='line'),  style={
                              'float': 'left', 'display': 'inline-block', 'width': '60%'}),
                     html.Div(dcc.Graph(id='radar'), style={
                              'float': 'right',                          'width': '40%'}),
                 ]
                 ),
    ]),

    html.Div(className='RightPad', style={'float': 'right', 'width': '35%'},  children=[
        html.Div(  # className='rightdown', #
            children=[
                html.Div(dcc.Dropdown(id='id_year', style={'width': '50%'},
                                      options=[{'label': i, 'value': i}
                                               for i in years],
                                      value=max(years))),
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
    # val = '2020'
    for i in range(len(pies)):
        # i=0
        df_fig = df[df['year'] == val]
        df_fig = df_fig.loc[:, [pies[i], 'Revenue']].groupby(
            by=[pies[i]], as_index=False).sum()
        df_fig['text'] = round(df_fig['Revenue']/1000000,
                               1).astype(str) + 'M'  # for hover text

        trace = go.Pie(
            labels=df_fig[pies[i]],
            values=df_fig['Revenue'],
            name='',
            text=df_fig['text'],
            textinfo='label+percent',
            hovertemplate="[%{label}]<br> Revenue: %{text}<br> Rate: %{percent}",
            hoverinfo='text',
            # textinfo 타입 (tangential / auto / horizontal / radial)
            insidetextorientation='tangential',
            hole=0.4,
            marker_colors=cols  # pie color
        )
        data = [trace]
        layout = go.Layout(
            title=pies[i], title_x=0.5, title_xanchor='center', showlegend=False,
            height=250, margin=dict(l=50, r=50, b=10, t=50)
        )
        fig = go.Figure(data, layout)
        figures.append(fig)

    return figures[0], figures[1], figures[2]


########## by Region
@dash_app.callback(
    [Output('idc_africa',  'figure'),
     Output('idc_america', 'figure'),
     Output('idc_asia',    'figure'),
     Output('idc_europe',  'figure'),
     Output('idc_oceania', 'figure')],
    [Input('id_year', 'value')])
def update_output(val):
    reg = df['Region'].unique()
    figures = []
    for i in range(len(reg)):
        # i =0
        df_fig = df[(df['year']==val) & (df['Region']==reg[i])]
        df_fig = round(df_fig.loc[:, ['Revenue', 'Margin']].sum(), 1)

        values = df_fig['Revenue']
        deltas = df_fig['Margin']

        trace = go.Indicator(
            mode='number+delta',
            # font size fixed (안하면 반응형으로 크기 제각각)
            title=dict(text=reg[i], font_size=20),
            delta=dict(
                reference=values - deltas,
                font_size=20,
                relative=False,
                increasing_color='#3078b4', increasing_symbol='',
                decreasing_color='#d13b40', decreasing_symbol='',
                position='top'
            ),
            number=dict(font_size=35),
            value=values,
        )
        data = [trace]
        layout = go.Layout(height=310)
        figure = go.Figure(data, layout)
        figures.append(figure)

    return figures[0], figures[1], figures[2], figures[3], figures[4]

### Bar


@dash_app.callback(Output('country', 'figure'), [Input('id_year', 'value')])
def update_output(val):

    # Sales by Country
    df_con = df[df['year'] == val]
    df_con = df_con.loc[:, ['Country', 'Revenue']].groupby(
        by=['Country'], as_index=False).sum()
    df_con = df_con.sort_values(by=['Revenue'], ascending=False)

    # Rank & Top 10
    df_con['rank'] = list(range(1, len(df_con['Country'])+1))
    df_con = df_con[df_con['rank'] <= 10].reset_index(drop=True)

    # hover_text
    df_con['text'] = df_con['Country'] + ': ' + \
        round(df_con['Revenue']/1000000, 1).astype(str) + 'M'

    trace = go.Bar(x=df_con['Country'],
                   y=df_con['Revenue'],
                   text=df_con['text'],
                   texttemplate='%{text}',
                   hoverinfo='text'
                   )

    data = [trace]

    layout = go.Layout(title='Country (Top 10)',
                       # title_x=0,
                       title_y=0.8,
                       height=310
                       )

    figure = {'data': data, 'layout': layout}

    return figure


### Line

### by YearMonth
@dash_app.callback(Output('line', 'figure'), [Input('id_year', 'value')])
def update_output(val):

    traces = []
    for yr in years:

        df_line = df[df['year'] == yr]
        df_line = df_line.loc[:, ['Revenue', 'year', 'month']].groupby(
            by=['year', 'month'], as_index=False).sum()

        # hover_text
        df_line['text'] = round(
            df_line['Revenue']/1000000, 1).astype(str) + 'M'

        traces.append(go.Scatter(x=df_line['month'],
                                 y=df_line['Revenue'],
                                 text=df_line['text'],
                                 hovertemplate='%{text}',
                                 mode='lines+markers',
                                 marker=dict(size=10),
                                 name=yr))
    data = traces

    layout = go.Layout(title='Revenue Trend (Monthly)',
                       # tick0 = 첫 번째 눈금의 배치 설정 (dtick과 함께 사용), dtick = 눈금 사이의 간격 설정
                       xaxis=dict(title='Month', tickmode='linear',
                                  tick0=1, dtick=1, showgrid=False),
                       legend=dict(orientation="h",    # option= 'v', 'h'
                                   xanchor="center",   # option= 'auto', 'left', 'center', 'right'
                                   # x= 0(left), 1 (right)
                                   x=0.5,
                                   yanchor="bottom",   # option= 'auto', 'top', 'middle', 'bottom'
                                   # 1.1,         # y= 1(top), -1(bottom)
                                   y=-1
                                   ),
                       height=320, margin=dict(l=50, r=10))

    figure = {'data': data, 'layout': layout}

    return figure


### Radar
### by Year & Category
@dash_app.callback(Output('radar', 'figure'), [Input('id_year', 'value')])
def update_output(val):

    df_rad = df.loc[:, ['Category', 'Revenue', 'year']].groupby(
        by=['year', 'Category'], as_index=False).sum()

    # Rank by 5 step Range
    df_rad['Rank'] = 0
    df_rad.loc[df_rad['Revenue'] < 10000000, 'Rank'] = 1
    df_rad.loc[(df_rad['Revenue'] >= 10000000) & (
        df_rad['Revenue'] < 30000000), 'Rank'] = 2
    df_rad.loc[(df_rad['Revenue'] >= 30000000) & (
        df_rad['Revenue'] < 50000000), 'Rank'] = 3
    df_rad.loc[(df_rad['Revenue'] >= 50000000) & (
        df_rad['Revenue'] < 70000000), 'Rank'] = 4
    df_rad.loc[(df_rad['Revenue'] >= 70000000), 'Rank'] = 5

    # range label - 순위별 범주 생성
    rad_rg = pd.DataFrame([[0, '0'], [1, '< 10M'], [
                          2, '10-30M'], [3, '30-50M'], [4, '50-70M'], [5, '70M <']])
    rad_rg.columns = ['Rank', 'Range']

    # Join
    df_radar = df_rad.merge(rad_rg, on='Rank', how='left')

    # Graph
    traces = []
    for yr in years:
        dat = df_radar[df_radar['year'] == yr]   # 특정 연도 추출
        ranks = list(dat['Rank'])                # 매출 순위 리스트
        ranks.append(ranks[0])                   # 마지막 연결부 추가
        thetas = list(dat['Category'])           # 상품 리스트
        thetas.append(thetas[0])                 # 마지막 연결부 추가
        rank_R = list(dat['Range'])              # 순위에 따른 범위정보
        rank_R.append(rank_R[0])                 # 마지막 연결부 추가

        traces.append(go.Scatterpolar(r=ranks,
                                      theta=thetas,
                                      name=yr,
                                      text=rank_R,
                                      hovertemplate="Revenue:%{text}"))

    data = traces
    layout = go.Layout(legend=dict(orientation="h",    # option= 'v', 'h'
                                   xanchor="center",   # option= 'auto', 'left', 'center', 'right'
                                   # x= 0(left), 1 (right)
                                   x=0.5,
                                   yanchor="bottom",   # option= 'auto', 'top', 'middle', 'bottom'
                                   # y= 1(top), -1(bottom)
                                   y=-1
                                   ),
                       height=320)

    figure = {'data': data, 'layout': layout}

    return figure


### Map
### Choropleth Map
@dash_app.callback(Output('map', 'figure'), [Input('id_year', 'value')])
def update_output(val):

    # Code3 by Country
    df_code = df.loc[:, ['Country', 'Code3']].drop_duplicates()

    # data
    df_map = df[df['year'] == val]
    df_map = df_map.loc[:, ['Country', 'Revenue']].groupby(
        by=['Country'], as_index=False).sum()

    # Join map & Code3
    df_m = df_map.merge(df_code, on='Country', how='left')

    # hover_text
    df_m['text'] = df_m['Country'] + ' - Total Revenue : ' + \
        round(df_m['Revenue']/1000000, 1).astype(str) + 'M'

    trace = go.Choropleth(
        locations=df_m['Code3'],
        z=df_m['Revenue'],
        text=df_m['text'],
        hoverinfo='text',          # 입력한 text만 활성화
        colorscale='Blues',        # color= Greens, Reds, Oranges, ...
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,

        # colorbar option = legend bar
        colorbar_title='Revenue ($)',
        colorbar_thickness=15,      # bar 너비 (default=30)
        colorbar_len=1,             # bar 길이 (default=1)
        # bar x 위치 (default=1.01, -2~3 사이값)
        colorbar_x=1.01,
        colorbar_ticklen=10         # bar 눈금 선 길이 (default=5)
    )

    data = [trace]
    layout = go.Layout(title='Sales Map',
                       geo=dict(showframe=False,
                                showcoastlines=False,
                                projection_type='equirectangular'),
                       height=420, margin=dict(l=50, r=50, b=20, t=50))

    figure = {'data': data, 'layout': layout}

    return figure


### Sankey
@dash_app.callback(Output('sankey', 'figure'), [Input('id_year', 'value')])
def update_output(val):

    # 2020년도 대륙 & 채널 & 상품별 매출 Flow 오름차순 정렬
    df_san = df[df['year'] == val].iloc[:, [13, 4, 11, 9]]
    df_san = df_san.sort_values(by=['Region', 'Channel', 'Category'])

    # label
    l_reg = list(df_san['Region'].unique())  # 5개 (순서 = 0 1 2 3 4)
    l_cha = list(df_san['Channel'].unique())  # 2개 (순서 = 5 6)
    l_cat = list(df_san['Category'].unique())  # 5개 (순서 = 7 8 9 10 11)
    labels = l_reg + l_cha + l_cat  # 12개 (순서 = 0 ~ 11)

    # source
    source1 = list(np.repeat(range(0, len(l_reg)), len(l_cha)))
    source2 = list(
        np.repeat(range(len(l_cat), len(l_cat)+len(l_cha)), len(l_cat)))
    sources = source1 + source2

    # target
    target1 = list(range(len(l_cat), len(l_cat) + len(l_cha))) * len(l_cat)
    target2 = list(range(len(l_cha) + len(l_cat), len(l_reg) +
                   len(l_cha) + len(l_cat))) * len(l_cha)
    targets = target1 + target2

    # value
    value1 = df_san.groupby(by=['Region', 'Channel'], as_index=False).sum()
    value2 = df_san.groupby(by=['Channel', 'Category'], as_index=False).sum()
    values = list(value1['Revenue']) + list(value2['Revenue'])

    trace = go.Sankey(node=dict(label=labels,
                                pad=15,
                                thickness=20,
                                line=dict(color='black', width=0.5),
                                color='#3078b4'),
                      link=dict(source=sources,
                                target=targets,
                                value=values,
                                color='#EAEAEA'))

    data = [trace]
    layout = go.Layout(title=dict(text='Sales Flow', font_size=16),
                       font_size=15,
                       height=420, margin=dict(l=50, r=50, b=20, t=50))

    figure = {'data': data, 'layout': layout}

    return figure



if __name__ == '__main__':
    dash_app.run_server(debug=False)
