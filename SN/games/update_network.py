import random
import initialization
import math

# از بین همسایگان، استراتژی برازنده ترین آنها به عنوان استراتژی دور بعد انتخاب میشود
def copy_fittest(network):
    for node in network.nodes():
        # update nodes
        maximum_fitness = 0
        fittest_mate = -1
        for mate in network.neighbors(node):
            if network.nodes[mate]['personality'].fitness > maximum_fitness:
                maximum_fitness = network.nodes[mate]['personality'].fitness
                fittest_mate = network.nodes[mate]['personality'].id
        # استراتژی برازنده ترین همسایه انتخاب می شود
        if not fittest_mate == -1:
            network.nodes[node]['personality'].new_strategy = network.nodes[fittest_mate]['personality']\
                .strategy

    # استراتژی های انتخاب شده به عنوان استراتژی مرحله بعد ثبت میشوند
    for node in network.nodes():
        network.nodes[node]['personality'].strategy = network.nodes[node]['personality'].new_strategy


def conditional_update(network):
    # احتمال تغییر استراتژی
    first = initialization.initialize.Person()
    second = initialization.initialize.Person()

    first.strategy = "D"
    second.strategy = "C"

    # احتمال اینکه بازین اول، استراتژی بازیکن دوم را انتخاب کند
    chance = 0
    if not first.strategy == second.strategy:
        # chance = 90 / 100
        homophily = 10
        noise_level = 1
        difference = (first.utiliy - second.utility) / (homophily * noise_level)
        chance = 1 / 1 + math.exp(difference)
    # متغیر تصادفی برای اعمال احتمال
    fate = random.randrange(0, 100) / 100
    if chance > fate:
        print("changed")
    else:
        print("not")


