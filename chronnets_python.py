import itertools
import networkx as nx
import os
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


def chronnet_create(df, self_loops= True, mode="directed"):
    time_seq = sorted(np.unique(df['time']))
    if len(time_seq) < 2:
        print("The total time interval in the dataset should be larger than two.")
    links = pd.DataFrame()
    cells_before=[]
    cells_after=[]
    weights = []
    for i in range(len(time_seq)-1):
        time1 = df[df.time == time_seq[i]]['cell'].tolist()
        time2 = df[df.time == time_seq[i+1]]['cell'].tolist()
        connections = list(itertools.product(time1, time2))
        cells_before.extend([connection[0] for connection in connections])
        cells_after.extend([connection[1] for connection in connections])
        weights.extend([1]*len(connections))
    links['from'] = cells_before
    links['to'] = cells_after
    links['weight'] = weights
    links = links.sort_values(by=['from', 'to']).reset_index().drop(columns = ['index'])
    links = links.groupby(['from', 'to'], as_index=False)['weight'].sum()
    net = nx.DiGraph()
    if len(links) !=0:
        net.add_nodes_from(np.unique(df['cell']))
        edgelist = []
        for index, rows in links.iterrows():
            edgelist.append(tuple([rows['from'], rows['to'], rows['weight']]))
        net.add_weighted_edges_from(edgelist)
        if self_loops == False:
            net.remove_edges_from(list(nx.selfloop_edges(net)))
        if mode == 'undirected':
            net = net.to_undirected()
    else:
        print("Empty graph returned.")
    return net


df_network = pd.DataFrame()
df_network['time'] = list(range(20))
df_network['cell'] = list(range(20))
net = chronnet_create(df_network)
nx.draw(net)
