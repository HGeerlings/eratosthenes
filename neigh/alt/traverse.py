"""
Exploring the use of plot.ly for visualizing correctness of a naive nearest-neighbor algorithm.
"""

from numpy.linalg import norm
import numpy as np
import operator
import random
import time

import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *

from neigh_perf import get_tsne_mapping

mapping = get_tsne_mapping()

def naive_nn(pt, pts):
    values = (norm(pt-other) for other in pts)
    # returns (min_index, min_value)
    return min(enumerate(values), key=operator.itemgetter(1))

def random_naive_neighbor_walk():
    """Simply to get a feel for timing of naive nearest-neighbor search.

    Sample without replacement from the mapping and find the naive_nn
    from all remaining points. Takes ~6 seconds.
    """
    indices = range(len(mapping))
    random.shuffle(indices)
    pts = [mapping[i]['pt'] for i in indices]
    while len(pts) > 1:
        naive_nn(pts.pop(), pts)

def init_progress_plot():
    stream_ids = tls.get_credentials_file()['stream_ids']

    unseen_pts = np.asarray([m['pt'] for m in mapping if 'seen' not in m])
    x, y = unseen_pts[:,0], unseen_pts[:,1]
    unseen_trace = Scatter(x=x, y=y, mode='markers',
                           stream=Stream(token=stream_ids[0]))

    seen_pts = np.asarray([m['pt'] for m in mapping if 'seen' in m])
    x, y = (seen_pts[:,0], seen_pts[:,1]) if len(seen_pts) else ([], [])
    seen_trace = Scatter(x=x, y=y, mode='markers',
                         stream=Stream(token=stream_ids[1]))

    data = Data([unseen_trace, seen_trace])
    layout = Layout(width=600, height=600)
    plot =  py.plot(Figure(data=data, layout=layout),
                   filename='erato-traversal-progress')

    stream = {'unseen': py.Stream(stream_ids[0]),
              'seen':  py.Stream(stream_ids[1])}
    for v in stream.values():
        v.open()

    return stream

# XXX: Mutates `mapping`, so you'll want to reload with
# `mapping = get_tsne_mapping()` on a new traverse().
def traverse(plotting=True, stream=None, plotting_delay=5):

    pt = random.choice(mapping)['pt']
    for i in range(len(mapping)):
        unseen = [m for m in mapping if 'seen' not in m]
        unseen_pts = np.asarray([m['pt'] for m in unseen])

        if plotting:
            # Update plot trace for unseen
            x, y = unseen_pts[:,0], unseen_pts[:,1]
            stream['unseen'].write(dict(x=x, y=y))

        nn_idx, nn_val = naive_nn(pt, unseen_pts) # find neighbor
        unseen[nn_idx]['seen'] = True # mark as seen
        pt = unseen[nn_idx]['pt'] # update current point

        if plotting:
            # Update plot trace for seen
            seen_pts = np.asarray([m['pt'] for m in mapping if 'seen' in m])
            x, y = (seen_pts[:,0], seen_pts[:,1]) if len(seen_pts) else ([], [])
            stream['seen'].write(dict(x=x, y=y))
            # Space out iterations so you can visually verify nearest-neighbor
            # selection
            time.sleep(plotting_delay)

if __name__ == "__main__":
    traverse(stream=init_progress_plot())
