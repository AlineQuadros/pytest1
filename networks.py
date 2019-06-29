# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 22:59:12 2019

@author: MyLAP
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# add EDGES with weight
g= nx.from_pandas_edgelist(rho_pos, 'keywords1', 'keywords2', 'spearman_cor')

# add NODES
g.add_nodes_from(ll)

# check
g.number_of_nodes()
g.number_of_edges()

# save for GEPHI
nx.write_gexf(g, "network_positive_correlations.gexf")

# check graph connectivity
nx.is_connected(g)
nx.number_connected_components(g)

comps = nx.connected_component_subgraphs(g)

# get NEIGHBORS
ego = "ant"
nodes = set([ego])
nodes.update(g.neighbors(ego))
egonet = g.subgraph(nodes)

