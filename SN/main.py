import networkx as nx
import matplotlib.pylab as plt
import initialize as init
import getting_inputs as gi
# import gui as interface
import play


nodes, edges = gi.main()
cooperatorsPercentage = 30

g = init.go(nodes, edges)
count = g.number_of_edges()
print("Edge count: " + str(count))
print("Strategy: " + str(init.find_node_by_id(1, g).strategy))
# ___________________________________________
# رسم شبکه
# options_2 = {
#  'with_labels': False,
#  'node_color': 'grey',
#  'node_size': 10,
#  'linewidths': 0,
#  'width': 0.1,
# }
#
# nx.draw_spring(g, iterations=100000, **options_2)
# plt.savefig('Network')
# plt.show()
# interface.go()

play.go(g)
for v in g.nodes():
    g.node[v]['state'] = str(v.fitness) + v.strategy
    # g.node[v]['dd'] = v.strategy
# g.node[1]['state'] = 'Y'
# g.node[2]['state'] = 'Y'

# for n in g.edges():
    # print(n)
    # g[n[0]][n[1]]['state'] = 'X'
# g.edge[2][3]['state'] = 'Y'


pos = nx.spring_layout(g)

nx.draw(g, pos)
node_labels = nx.get_node_attributes(g, 'state')
nx.draw_networkx_labels(g, pos, labels=node_labels)

# edge_labels = nx.get_edge_attributes(g, 'state')
# nx.draw_networkx_edge_labels(g, pos, labels=edge_labels)
plt.savefig('this.png')
plt.show()

