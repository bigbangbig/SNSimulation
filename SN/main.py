import networkx as nx
import matplotlib.pylab as plt
import initialization.initialize as init
import initialization.getting_inputs as gi
# import gui as interface
import games.play as play
import plots.main as plots


# tkinter برای اینترفیس
# py2exe برای ساختن فایل اجرایی برای ویندوز

nodes, edges = gi.main()
cooperatorsPercentage = 40
g = init.go(nodes, edges, cooperatorsPercentage)
count = g.number_of_edges()
# print("Edge count: " + str(count))
# print("Strategy: " + str(init.find_node_by_id(1, g).strategy))
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

# اطلاعات اولیه گراف را ذخیره میکند. مثل تعداد گره ها
plots.init(g)

# بازی به تعداد مشخص شده در رنج بین همه گره ها انجام میشود
for i in range(1000):
    play.go(g)
    plots.save_network_info(g, i + 1)

# رسم نمودار تعداد همکاری کنندگان
plots.plot()

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
plt.savefig('Images/Network.png')
plt.show()

