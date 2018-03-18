#figure1
from plotly.offline import plot, iplot
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)

import numpy as np

import pandas as pd

import quandl

x_values_1 = ['X8','X7','X6','X5']
x_values_2 = ['X4','X3','X2','X1']

y_values_1 = [20,18,45,18]
y_values_2 = [-35,-5,-15,-45]

trace_1 = go.Bar(y=x_values_1,x=y_values_1, name="<b>Negative</b>",orientation="h",marker=dict(
    color="red", 
    line=dict(color='black',
              width=1.5)))
trace_2 = go.Bar(y=x_values_2,x=y_values_2, name="Positive",orientation="h",marker=dict(color="blue",line=dict(color='black',
                 width=1.5)))

layout = dict(title = 'Correlations With  Employees Probabolity of Churn',
             yaxis=dict(title="Variable"))
#layout = dict(barmode = 'stack')

data = [trace_1,trace_2]
figure1 = dict(data=data,layout=layout)
