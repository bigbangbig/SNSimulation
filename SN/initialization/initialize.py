import networkx as nx
import numpy as np
import utilities.search as search


class Person:
    def __init__(self):
        self._strategy = None
        self._new_strategy = None
        self._ID = None
        self._Fitness = 0

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    @property
    def new_strategy(self):
        return self._new_strategy

    @new_strategy.setter
    def new_strategy(self, new_strategy):
        self._new_strategy = new_strategy

    @property
    def id(self):
        return self._ID

    @id.setter
    def id(self, id_value):
        self._ID = id_value

    @property
    def fitness(self):
        return self._Fitness

    @fitness.setter
    def fitness(self, fitness_value):
        self._Fitness = fitness_value


def create_network(node_count, percentage):
    g = nx.Graph()
    how_many = int((node_count * percentage) / 100)
    for i in range(node_count):
        person = Person()
        if i < how_many:
            person.strategy = "C"
        else:
            person.strategy = "D"
        person.id = i
        g.add_node(person)
    return g


def link(network, first, second):
    first = search.find_node_by_id(first, network)
    second = search.find_node_by_id(second, network)
    network.add_edge(first, second, state="hi")
    # network.add_edge(first, second)


def has_link(network, _first, _second):
    first = search.find_node_by_id(_first, network)
    second = search.find_node_by_id(_second, network)
    if network.has_edge(first, second):
        return True
    else:
        return False


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
        while has_link(network, first, second):
            first = np.random.randint(0, count)
            second = np.random.randint(0, count)

        link(network, first, second)
    return network


def go(node_count, link_count, percentage):
    net = create_network(node_count, percentage)
    res = create_random_links(net, link_count)
    return res

#
# def set_strat(network, coopersPercent):
