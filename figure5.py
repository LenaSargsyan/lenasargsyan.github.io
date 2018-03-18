from plotly.offline import plot, iplot
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)
import plotly.plotly as py
import plotly.figure_factory as ff

import numpy as np

import pandas as pd

import quandl

#figure5


df = [dict(Task="Task 1", Start='2018-01-01', Finish='2018-02-01', Resource='Idea Validation'),
      dict(Task="Task 2", Start='2018-03-05', Finish='2018-04-01', Resource='Team Formation'),
      dict(Task="Task 3", Start='2018-04-01', Finish='2018-09-30', Resource='Prototyping')]
colors = ['#7a0504', (0.2, 0.7, 0.3), 'rgb(210, 60, 180)']

figure5 = ff.create_gantt(df, colors=colors, index_col='Resource', reverse_colors=True, show_colorbar=True,
                          title='Startup Roadmap')
