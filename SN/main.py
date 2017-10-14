import networkx as nx
import matplotlib.pylab as plt
import initialize as init
import getting_inputs as gi


nodes, edges = gi.main()
g = init.go(nodes, edges)
count = g.number_of_edges()
print("Edge count: " + str(count))

# ___________________________________________
# رسم شبکه
options_2 = {
 'with_labels': False,
 'node_color': 'grey',
 'node_size': 10,
 'linewidths': 0,
 'width': 0.1,
}

nx.draw_spring(g, iterations=100000, **options_2)
plt.savefig('Network')
plt.show()

