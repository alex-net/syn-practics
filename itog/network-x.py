# https://stackoverflow.com/questions/20133479/how-to-draw-directed-graphs-using-networkx-in-python
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


# #---directed graph---
# G = nx.DiGraph(directed=True)

# # add nodes
# G.add_node("Singapore")
# G.add_node("San Francisco")
# G.add_node("Tokyo")
# G.add_nodes_from(["Riga", "Copenhagen"])

# # add edges
# G.add_edge("Singapore","San Francisco")
# G.add_edge("San Francisco","Tokyo")
# G.add_edges_from(
#     [
#         ("Riga","Copenhagen"),
#         ("Copenhagen","Singapore"),
#         ("Singapore","Tokyo"),
#         ("Riga","San Francisco"),
#         ("San Francisco","Singapore"),
#     ]
# )
def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)

plt.figure()
plt.subplot(151)
plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

plt.subplot(221)
plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
plt.show()

