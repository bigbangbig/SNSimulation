import networkx as nx
import numpy as np
import utilities.search as search
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


# ایجاد لیستی از افراد با تعداد مشخص و درصد اولیه مشخص
def create_people(node_count, percentage):
    people = []
    how_many = int((node_count * percentage) / 100)
    for i in range(node_count):
        person = Person()
        if i < how_many:
            person.strategy = "C"
            person.new_strategy = "C"
        else:
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


def go(node_count, percentage):

    net = create_scale_free(node_count)
    peoples_list = create_people(node_count, percentage)

    # لیست ایجاد شده از افراد به یک دیکشنری تبدیل میشود تا بتوان در تابع set_node_attributes از آن استفاده کرد
    people = {key: value for (key, value) in enumerate(peoples_list)}

    nx.set_node_attributes(net, people, 'personality')

    return net


def create_scale_free(node_count):
    power_law_sequence = nx.utils.powerlaw_sequence(node_count, exponent=2.0)
    seq_sum = 0

    # برخی از اعداد ایجاد شده در توسط تابع powerlaw_sequence ممکن است کمتر از 1 باشند
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

    for i in range(node_count):
        if g.degree(i) == 0:
            print("dddddduuuuude")
    return g
