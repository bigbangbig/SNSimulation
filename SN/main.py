import networkx as nx
import matplotlib.pylab as plt
import initialize as init
import getting_inputs as gi
# import interface as gui

nodes, edges = gi.main()
cooperatorsPercentage = 40

# gui()
g = init.go(nodes, edges, cooperatorsPercentage)
limit = int(nodes * (cooperatorsPercentage / 100))
count = g.number_of_edges()
print("Edge count: " + str(count))
print("Strategy of node 1: " + str(init.find_node_by_id(1, g).strategy))
string = "Strategy of node %d: " + str(init.find_node_by_id(limit, g).strategy)
print(string % limit)
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

