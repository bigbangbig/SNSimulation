import networkx as nx
import matplotlib.pylab as plt

G = nx.erdos_renyi_graph(100, 0.15)
nx.draw(G)
plt.savefig('Hi')