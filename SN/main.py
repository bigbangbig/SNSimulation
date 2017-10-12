import networkx as nx
import matplotlib.pylab as plt
import initialize as init


g = init.go(50, 150)
count = g.number_of_edges()
print("Node count: " + str(count))

options_2 = {
 'with_labels': False,
 'node_color': 'grey',
 'node_size': 10,
 'linewidths': 0,
 'width': 0.1,
}

nx.draw_spring(g, iterations=1, **options_2)

# nx.draw_random(g)
plt.savefig('Hi')
plt.show()

