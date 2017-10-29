import matplotlib.pyplot as plt

# متغیرهای عمومی برای ذخیره اطلاعات
cooperators_in_round = []
node_count = 0


# رسم نمودار تعداد همکاری کنندگان بر حسب دورهای بازی
def plot():
    x = [x[0] for x in cooperators_in_round]
    y = [x[1] for x in cooperators_in_round]
    plt.ylim([0, node_count])
    plt.title("Cooperators in each round of the game")
    plt.ylabel("Cooperators")
    plt.xlabel("Round Number")
    plt.plot(x, y)
    plt.savefig("plots/Images/Cooperators")
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


def init(network):
    global node_count
    node_count = len(network.nodes)

