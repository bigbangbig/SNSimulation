import networkx as nx
import numpy as np


def create_network(node_count):
    g = nx.Graph()
    for i in range(node_count):
        g.add_node(i)
    return g


def link(network, first, second):
    network.add_edge(first, second)


def create_random_links(network, how_many):
    count = network.number_of_nodes()

    complete_graph_nodes = (count * (count - 1))/2
    # در صورتی که تعداد درخواستی از تعداد یال های گراف کامل بیشتر باشد
    if how_many > int(complete_graph_nodes):
        # مقدار درخواستی تنظیم میشود
        how_many = int(complete_graph_nodes)

    for i in range(how_many):
        first = np.random.randint(0, count)
        second = np.random.randint(0, count)

        # تا وقتی که یالی که مبدا و مقصد آن به صورت تصادفی انتخاب شده در گراف وجود داشته باشد
        # محاسبه مبدا و مقصد مجدداً انجام میشود
        while network.has_edge(first, second):
            first = np.random.randint(0, count)
            second = np.random.randint(0, count)

        link(network, first, second)
    return network


def go(node_count, link_count):
    net = create_network(node_count)
    res = create_random_links(net, link_count)
    return res
