import networkx as nx
import matplotlib.pylab as plt
import initialize as init


def get_input(node, edge):
    try:
        node = int(input("How many nodes? "))
        edge = int(input("How many edges? "))
        return True, node, edge
    except Exception:
        print("Exception thrown. Did you enter numbers? this only accepts numbers")
        return False, node, edge


nodes = 0
edges = 0
res = False
while not res:
    res, nodes, edges = get_input(nodes, edges)
    # if res:
    #     break

g = init.go(nodes, edges)
count = g.number_of_edges()
print("Edge count: " + str(count))

options_2 = {
 'with_labels': False,
 'node_color': 'grey',
 'node_size': 10,
 'linewidths': 0,
 'width': 0.1,
}

nx.draw_spring(g, iterations=1, **options_2)

# nx.draw_random(g)
plt.savefig('Network')
plt.show()

