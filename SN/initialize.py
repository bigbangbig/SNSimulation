import networkx as nx
import numpy as np


class People:
    def __init__(self):
        self._strategy = None
        self._ID = None

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    @property
    def id(self):
        return self._ID

    @id.setter
    def id(self, id_value):
        self._ID = id_value


def create_network(node_count):
    g = nx.Graph()
    for i in range(node_count):
        person = People()
        person.strategy = "D"
        person.id = i
        g.add_node(person)
    return g


def find_node_by_id(_id, network):
    nodes = network.nodes()
    for x in nodes:
        if x.id == _id:
            break
    else:
        x = None
    return x


def link(network, first, second):
    first = find_node_by_id(first, network)
    second = find_node_by_id(second, network)
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

#
# def set_strat(network, coopersPercent):
