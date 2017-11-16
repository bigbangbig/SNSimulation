import networkx as nx
import numpy as np
import utilities.search as search
import operator
import random

class Person:
    def __init__(self):
        self._strategy = None
        self._new_strategy = None
        self._ID = None
        self._Fitness = 0
        self._utility = 0

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    # استراتژی مرحله بعد در این فیلد ذخیره میشود
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

    @property
    def utility(self):
        return self._utility

    @utility.setter
    def utility(self, util_value):
        self._utility = util_value


# ایجاد لیستی از افراد با تعداد مشخص
def create_people(node_count):
    people = []
    for i in range(node_count):
        person = Person()
        person.strategy = "D"
        person.new_strategy = "D"
        person.id = i
        people.append(person)
    return people


# DEPRECATED
# ایجاد یال بین دو گره داده شده
def link(network, first, second):
    first = search.find_node_by_id(first, network)
    second = search.find_node_by_id(second, network)
    network.add_edge(first, second, state="hi")
    # network.add_edge(first, second)


# بررسی اینکه آیا در شبکه، بین گره های مشخص شده یال هست یا نه
def has_link(network, _first, _second):
    first = search.find_node_by_id(_first, network)
    second = search.find_node_by_id(_second, network)
    if network.has_edge(first, second):
        return True
    else:
        return False


# DEPRECATED
# برای ساختن لینک های تصادفی به تعداد مشخص
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


def set_cooperators(network, percentage, position):
    node_count = len(network.nodes())
    how_many = int((node_count * percentage) / 100)
    counter = 0
    centrality_values = nx.get_node_attributes(network, 'state')

    if position == 'c':
        sorted_centralities = reversed(sorted(centrality_values.items(), key=operator.itemgetter(1)))
    elif position == 'e':
        sorted_centralities = sorted(centrality_values.items(), key=operator.itemgetter(1))
    else:
        while counter < how_many:
            node = random.choice(list(network.nodes()))
            if not network.nodes[node]['personality'].strategy == "C":
                network.nodes[node]['personality'].strategy = "C"
                network.nodes[node]['personality'].new_strategy = "C"
                counter += 1
        return network

    for (node, centrality) in sorted_centralities:
        if counter < how_many:
            network.nodes[node]['personality'].strategy = "C"
            network.nodes[node]['personality'].new_strategy = "C"
            counter += 1
        else:
            break
    return network


def go(node_count, percentage, position):

    clusters = 3
    size = int(node_count / clusters)
    net1 = create_scale_free(size + (node_count - (size * 3)))
    for i in range(clusters - 1):
        print(len(net1))
        gg = create_scale_free(size)
        net1 = nx.disjoint_union(net1, gg)
    net = create_scale_free(node_count)
    net = net1
    if not nx.is_connected(net):
        print("Network is not connected. Attempting to connect the components..")
        component_counter = 0
        components = sorted(nx.connected_component_subgraphs(net), key=len)
        for c in range(len(components)):
            if component_counter == 0:
                component_counter += 1
                continue
            else:
                net.add_edge(next(iter(components[component_counter].nodes())),
                           next(iter(components[component_counter - 1].nodes())))
                component_counter += 1
    print(len(net.nodes()))
    peoples_list = create_people(node_count)

    # لیست ایجاد شده از افراد به یک دیکشنری تبدیل میشود تا بتوان در تابع set_node_attributes از آن استفاده کرد
    people = {key: value for (key, value) in enumerate(peoples_list)}

    nx.set_node_attributes(net, people, 'personality')

    # محاسبه مرکزیت بردار ویژه
    # در صورت رخ دادن exception تا 10 بار محاسبه مجددا انجام میشود
    # while True:
    #     counter = 0
    #     try:
    #         if counter > 10:
    #             print("Eigenvector centrality calculation stopped with errors. ")
    #             break
    #
    #         bb = nx.eigenvector_centrality(net)
    #         nx.set_node_attributes(net, bb, 'state')
    #
    #     except nx.exception.PowerIterationFailedConvergence:
    #         continue
    #     break
    #     counter += 1
    try:
        bb = nx.eigenvector_centrality(net)
        nx.set_node_attributes(net, bb, 'state')

    except nx.exception.PowerIterationFailedConvergence:
        print("hi")

    first_generation = set_cooperators(net, percentage, position)

    return first_generation


def create_scale_free(node_count):
    power_law_sequence = nx.utils.powerlaw_sequence(node_count, exponent=2.0)
    seq_sum = 0

    # clusters_list[0] = nx.utils.powerlaw_sequence(size + (node_count - (size * clusters)), exponent=2.0)
    # تعداد زیادی از اعداد ایجاد شده توسط تابع powerlaw_sequence کمتر از 1 خواهند بود
    # چون هدف بررسی انتشار همکاریست، نیاز داریم که همه نودها با هم ارتباط داشته باشند
    # پس هر نود باید حداقل یک یال داشته باشد
    for i in range(node_count):
        power_law_sequence[i] = int(power_law_sequence[i]) + 1
        seq_sum += power_law_sequence[i]

    # تابع configuration_model به مجموع فرد نیاز دارد
    if seq_sum % 2 != 0:
        power_law_sequence[0] += 1

    g = nx.configuration_model(power_law_sequence)
    g = nx.Graph(g)
    g.remove_edges_from(g.selfloop_edges())

    # با این که حداقل تعداد یالها 1 در نظر گرفته شده
    # ممکن است با ایجاد یک چند ضلعی بدون قطر، گراف همبند نباشد (در یکی از اجراها یک مثلث جدا مشاهده شد)
    # در این قسمت، وجود چند مولفه همبندی بررسی شده، و در صورت نیاز بین آنها اتصال برقرار خواهد شد
    if not nx.is_connected(g):
        print("Network is not connected. Attempting to connect the components..")
        component_counter = 0
        components = sorted(nx.connected_component_subgraphs(g), key=len)
        for c in range(len(components)):
            if component_counter == 0:
                component_counter += 1
                continue
            else:
                g.add_edge(next(iter(components[component_counter].nodes())),
                           next(iter(components[component_counter - 1].nodes())))
                component_counter += 1

    return g
