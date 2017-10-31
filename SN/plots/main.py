import networkx as nx
import matplotlib.pyplot as plt

# متغیرهای عمومی برای ذخیره اطلاعات
cooperators_in_round = []
node_count = 0


# رسم نمودار تعداد همکاری کنندگان بر حسب دورهای بازی
def plot():
    x = [x[0] for x in cooperators_in_round]
    y = [x[1] for x in cooperators_in_round]
    plt.ylim([0, node_count + int((node_count * 10) / 100)])
    plt.title("Cooperators in each round of the game")
    plt.ylabel("Cooperators")
    plt.xlabel("Round Number")
    plt.plot(x, y)
    plt.savefig("Images/Cooperators")
    plt.show()


# شماره دور بازی و گراف شبکه را به صورت ورودی دریافت می کند
def save_network_info(network, game_round):
    cooperators = 0
    # تعداد همکاری کنندگان را محاسبه کرده
    for i in network.nodes:
        if i.strategy == "C":
            cooperators += 1
    global cooperators_in_round
    # و این تعداد را به همراه شماره دور کنونی در یک لیست ذخیره می کند
    cooperators_in_round.append((game_round, cooperators))


# اطلاعات شبکه اولیه را ذخیره میکند
def init(network):
    global node_count
    node_count = len(network.nodes)


# گراف شبکه را به عنوان ورودی دریافت کرده آن را رسم میکند
def show_network(g):
    # برای هر گره استراتژی و برازندگی هر یک از گره ها محاسبه شده
    # و به صورت برچسب در هر گره نمایش داده میشود
    for v in g.nodes():
        g.node[v]['state'] = str(v.fitness) + v.strategy

    pos = nx.spring_layout(g)

    plt.figure(figsize=(12, 8))
    nx.draw(g, pos)
    node_labels = nx.get_node_attributes(g, 'state')
    nx.draw_networkx_labels(g, pos, labels=node_labels)

    # edge_labels = nx.get_edge_attributes(g, 'state')
    # nx.draw_networkx_edge_labels(g, pos, labels=edge_labels)
    plt.savefig('Images/Network.png')
    plt.show()


