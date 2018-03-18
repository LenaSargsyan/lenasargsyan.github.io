import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import quandl
import pandas as pd

import plotly.graph_objs as go

import figure1
import figure5
quandl.ApiConfig.api_key = "g621vWh9j9bPtzWZYTDa"
app = dash.Dash()
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})


title = html.H1("Homework 5",style={'color':'red', 'fontFamily':"Comic Sans MS","textAlign":'center'}, className='row')

churnStatistics = dcc.Graph(id="churn_statistics", figure=figure1.figure1)
projectRoadmap = dcc.Graph(id="project_roadmap", figure=figure5.figure5)



GOOGLE_KEY = 0
BITCOIN_KEY = 1
APPLE_KEY = 2
MICROSOFT_KEY = 3
FACEBOOK_KEY = 4

facebook_data = quandl.get("WIKI/FB", authtoken="g621vWh9j9bPtzWZYTDa")
apple_data = quandl.get("WIKI/AAPL", authtoken="g621vWh9j9bPtzWZYTDa")
google_data = quandl.get("WIKI/GOOGL", authtoken="g621vWh9j9bPtzWZYTDa")
bitcoin_data = quandl.get("BCHARTS/ABUCOINSUSD", authtoken="g621vWh9j9bPtzWZYTDa")
microsoft_data = quandl.get("WIKI/MSFT", authtoken="g621vWh9j9bPtzWZYTDa")

facebook_values = round(facebook_data.Open.pct_change().head()[1:], 3)
apple_values = round(apple_data.Open.pct_change().head()[1:], 3)
google_values = round(google_data.Open.pct_change().head()[1:], 3)
bitcoin_values = round(bitcoin_data.Open.pct_change().head()[1:], 3)
microsoft_values = round(microsoft_data.Open.pct_change().head()[1:], 3)


my_data = quandl.get("FRED/GDP")


app.layout = html.Div([
    html.Div([
        html.Div([
    
            title,
    
            html.Div([
                html.Div([dcc.RadioItems(
                    id = 'radiobutton',
                    options=[
                        {'label': 'Employee Churn', 'value': 0},
                        {'label': 'Startup RoadMap', 'value': 1}
                        ],
                    ),
                ], className='three columns'),
               
                html.Div([], id = 'radiogroup_graph_container_div',className='nine columns')
            ],
            className='row'
            ),
        ])
    ],
    className='row'),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id = 'dropdown',
                options=[   
                    {'label': 'Google', 'value': GOOGLE_KEY},
                    {'label': 'Bitcoin', 'value': BITCOIN_KEY},
                    {'label': 'Apple', 'value': APPLE_KEY},
                    {'label': 'Microsoft', 'value': MICROSOFT_KEY},
                    {'label': 'Facebook', 'value': FACEBOOK_KEY}

                ],
                multi=True,
                placeholder="Please, select a stok",
                className='row'),
            html.Div([], id = "dropdown_graph_container_div", className = 'row')
        ],className = 'row')
    ],
    className='row'),
    html.Div([
        html.Div([
            dcc.Graph(id='graph'),
            
            dcc.RangeSlider(
            id = 'range_slider',
            min=0,
            max=len(my_data.index),
            value=[0, len(my_data.index)]
            ),
        ])  
  ],
    className='row'),
],
className='row')


@app.callback(
    Output(component_id='radiogroup_graph_container_div', component_property='children'),
    [Input(component_id='radiobutton', component_property='value')],
    )
def update_graph(radio_btn_value):
    if radio_btn_value==0:
        return churnStatistics
    elif radio_btn_value==1:
        return projectRoadmap



@app.callback(
    Output(component_id='dropdown_graph_container_div', component_property='children'),
    [Input(component_id='dropdown', component_property='value')]
)
def update_graph(stock_value):
    headerArray = []
    cellsArray = []
    boxData = []
    if len(stock_value) > 0 and len(stock_value)< 3:
        for key in stock_value:
            if(key==GOOGLE_KEY):
                headerArray.append('Google')
                cellsArray.append(google_values)
                boxData.append(go.Box(x=google_data.Open.pct_change(), name = '<b>Google</b>'))
            elif(key==BITCOIN_KEY):
                headerArray.append('Bitcoin')
                cellsArray.append(bitcoin_values)
                boxData.append(go.Box(x=bitcoin_data.Open.pct_change(), name = '<b>Bitcoin</b>'))
            elif(key==APPLE_KEY):
                headerArray.append('Apple')
                cellsArray.append(apple_values)
                boxData.append(go.Box(x=apple_data.Open.pct_change(), name = '<b>Apple</b>'))
            elif(key==MICROSOFT_KEY):
                headerArray.append('Microsoft')
                cellsArray.append(microsoft_values)
                boxData.append(go.Box(x=microsoft_data.Open.pct_change(), name = '<b>Microsoft</b>'))
            elif(key==FACEBOOK_KEY):
                headerArray.append('Facebook')
                cellsArray.append(facebook_values)
                boxData.append(go.Box(x=facebook_data.Open.pct_change(), name = '<b>Amazon</b>'))            
        
        parentDiv = html.Div([getBox(boxData), getTable(headerArray, cellsArray)],className='row')
        return parentDiv

    elif len(stock_value) >= 3:
        return parentDiv

    else: return



def getBox(boxData):
    boxLayout = dict(title = 'Distribution of Price churn')
    boxFigure = dict(data=boxData, layout=boxLayout)
    box = html.Div([dcc.Graph(id="box", figure=boxFigure)])
    return box

def getTable(headerArray, cellsArray):

    header = dict(values=headerArray,
              align = ['center','center'],
              font = dict(color = 'white', size = 12),
              fill = dict(color='#119DFF')
             )
    cells = dict(values=cellsArray,
             align = ['center','center'],
             fill = dict(color=["yellow","white"])
            )  

    trace = go.Table(header=header, cells=cells)
    data = [trace]
    layout = dict(width=500, height=300)
    figure = dict(data=data, layout=layout)
    table = html.Div([dcc.Graph(id="google_bitcoin_statistics_table", figure=figure)])
    return table



@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='range_slider', component_property='value')]
)
def update_graph(input_value):
    modified_index = my_data.index[input_value[0]:input_value[1]]
    modified_values = my_data.Value[input_value[0]:input_value[1]]

    data = [go.Scatter(x=modified_index,y=modified_values,fill="tozeroy")]
    layout = dict(title = '<b>US GDP over time</b>')
    figure = dict(data=data, layout = layout)
    return figure



if __name__ == '__main__':
    app.run_server()