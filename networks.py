# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 22:59:12 2019

@author: MyLAP
"""

import networkx as nx
import pandas as pd
import string


#!  import datasets with Spearman correlations
rho_dt = pd.read_csv('rho_dataset.csv', sep=',')

# ----------------------prepare data for NETWORKx-----------------------------

# filter per minimum correlation coefficient and TODO p<0.05
rho_pos = pd.DataFrame()
rho_neg = pd.DataFrame()
rho_pos = rho_dt[rho_dt[0] > 0.7]
rho_neg = rho_dt[rho_dt[0] < -0.01]

# fix index and keyword columns - POSITIVE CORR
rho_pos["keywords"] = rho_pos.index
rho_pos["keywords"] = rho_pos["keywords"].astype("str")
temp2 = rho_pos["keywords"].str.split(',', expand=True)
temp2.columns = ['keywords1', 'keywords2']

rho_pos = rho_pos.assign(keywords1=temp2['keywords1'])
rho_pos = rho_pos.assign(keywords2=temp2['keywords2'])
rho_pos = rho_pos.drop(columns='keywords')

rho_pos.columns = ['spearman_cor','keywords1', 'keywords2']

rho_pos.keywords1 = rho_pos.keywords1.str.replace('[{}]'.format(string.punctuation), '')
rho_pos.keywords2 = rho_pos.keywords2.str.replace('[{}]'.format(string.punctuation), '')
rho_pos.keywords1 = rho_pos.keywords1.str.strip()
rho_pos.keywords2 = rho_pos.keywords2.str.strip()

rho_pos.describe()

# fix index and keyword columns - NEGATIVE CORR
rho_neg["keywords"] = rho_neg.index
rho_neg["keywords"] = rho_neg["keywords"].astype("str")
temp2 = rho_neg["keywords"].str.split(',', expand=True)
temp2.columns = ['keywords1', 'keywords2']

rho_neg = rho_neg.assign(keywords1=temp2['keywords1'])
rho_neg = rho_neg.assign(keywords2=temp2['keywords2'])
rho_neg = rho_neg.drop(columns='keywords')

rho_neg.columns = ['spearman_cor','keywords1', 'keywords2']

rho_neg.keywords1 = rho_neg.keywords1.str.replace('[{}]'.format(string.punctuation), '')
rho_neg.keywords2 = rho_neg.keywords2.str.replace('[{}]'.format(string.punctuation), '')
rho_neg.keywords1 = rho_neg.keywords1.str.strip()
rho_neg.keywords2 = rho_neg.keywords2.str.strip()

rho_neg.describe()

#number of unique keywords after filtering
nodes_pos = pd.concat([rho_pos["keywords1"],rho_pos["keywords2"]])
nodes_pos.nunique()

nodes_neg = pd.concat([rho_neg["keywords1"],rho_neg["keywords2"]])
nodes_neg.nunique()

# ----------------------------- networkx ------------------------------------

# add EDGES with weight
g_pos= nx.from_pandas_edgelist(rho_pos, 'keywords1', 'keywords2', 'spearman_cor')
g_neg= nx.from_pandas_edgelist(rho_neg, 'keywords1', 'keywords2', 'spearman_cor')
# add NODES
g_pos.add_nodes_from(nodes_pos.unique(), name=nodes_pos.unique())
g_neg.add_nodes_from(nodes_neg.unique(), name=nodes_neg.unique())
# check
g_pos.number_of_nodes()
g_pos.number_of_edges()
g_neg.number_of_nodes()
g_neg.number_of_edges()
# save for GEPHI
nx.write_gexf(g_pos, "network_positive_correlations.gexf")
nx.write_gexf(g_neg, "network_negative_correlations.gexf")

# check graph connectivity
#nx.is_connected(g_pos)
#nx.number_connected_components(g_pos)
#nx.number_connected_components(g_neg)
#comps = nx.connected_component_subgraphs(g_pos)

# get list top 20 nodes (based on degree)
degrees = [val for (node, val) in g_pos.degree()]
degrees = pd.DataFrame(degrees)
#join node name
degrees['name'] = nodes_pos.unique()


# get Edges 
ego = "swan lake"
nodes = set([ego])
nodes.update(g_pos.neighbors(ego))
egonet = [val for (node, val) in g_pos.neighbors(ego).degree()]

