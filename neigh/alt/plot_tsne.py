import plotly.plotly as py
from plotly.graph_objs import *

def plot_tsne(X_2d):
    trace = Scatter(
        x=X_2d[:,0],
        y=X_2d[:,1],
        mode='markers')
    data = Data([trace])
    return py.plot(data, filename='tsne-mapping')
