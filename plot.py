# Run this app with python and visit http://127.0.0.1:8050/ in your web browser.

import pandas
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import plotly.express as px
from dash import Dash, html, dcc, dash_table
import plotly.express as px

PATH=os.environ['OUT_PATH']
schema_tda_current_assets=['date', 'accountid', 'symbol', 'units', 'value']
schema_tda_current_networth=['date', 'accountid', 'value']
schema_tda_trades=['accoutid', 'date', 'symbol', 'units', 'value', 'description']
schema_tda_historical_networth = ['date', 'accountid', 'value']

# def plot_bar(x, y):
#     fig = plt.figure()
#     fig.set_dpi(300)

#     ax = fig.add_axes([0,0,1,1])
#     fmt = '${x:,.0f}'
#     tick = mtick.StrMethodFormatter(fmt)
#     ax.xaxis.set_major_formatter(tick)
#     bars = ax.barh(x, y)
#     ax.bar_label(bars)
#     plt.show()

# def plotly_bar(header, x, y):
#     fig = px.bar(data_frame=header, x = x, y = y)
#     fig.show()

def plotholdings():
    data = pandas.read_csv(PATH+'/tda_current_assets.csv', sep='\s*,\s*', engine='python', \
        header=None, names=schema_tda_current_assets)
    print(data)
    return px.bar(data_frame=data, labels=dict(symbol='Stock Ticker', value='Value ($)'), x='symbol', y='value', \
        title='Holdings')

def plottimeseries():
    data = pandas.read_csv(PATH+'/tda_current_networth.csv', sep='\s*,\s*', engine='python', \
        dtype={"accountid":str}, header=None, names=schema_tda_current_networth)

    # plot_bar(data['accountid'], data['value'])
    fig = px.bar(data_frame=data, labels=dict(symbol='Account ID', value='Value ($)'), x='accountid', y='value', \
        title='Account Values')
    return fig

def plottrades():
    data = pandas.read_csv(PATH+'/tda_trades.csv', sep='\s*,\s*', engine='python', header=None, names=schema_tda_trades)
    return data
    # fig, ax = plt.subplots()
    # fig.set_dpi(300)
    # # hide axes
    # fig.patch.set_visible(False)
    # ax.axis('off')
    # ax.axis('tight')
    # ax.table(cellText=data.values, colLabels=data.columns, loc='center')

    #fig.tight_layout()

    # plt.show()

# plotholdings()
# plottimeseries()
# plottrades()

app = Dash(__name__)

df = plottrades()
style={'width': '90vw', 'margin-left': 'auto',\
            'margin-right': 'auto'}
app.layout = html.Div(style=style, children=[
    html.H1(children='TD Ameritrade Account Status'),

    #html.Div(children='''Chart 1'''),

    dcc.Graph(id='holdings', figure=plotholdings(), style = style),
    #html.Div(children='''Chart 2'''),

    dcc.Graph(id='timeseries', figure=plottimeseries(), style=style),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i}
            for i in df.columns],
        data=df.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender"),
        sort_action='native'
    ), 
])

if __name__ == '__main__':
    app.run_server(debug=True)
