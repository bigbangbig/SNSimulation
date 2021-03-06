import random
import math
import operator


# از بین همسایگان، استراتژی برازنده ترین آنها به عنوان استراتژی دور بعد انتخاب میشود
from jsonschema._validators import enum


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


def conditional_update(network, homophily, method):
    # homophily = 1
    noise_level = 1

    for node in network.nodes():
        position = network.nodes[node]
        person = network.nodes[node]['personality']
        # شانس تغییر استراتژی برای تمامی همسایه ها محاسبه میشود
        # بیشترین مقدار در این متغیر قرار میگیرد
        maximum_chance = 0
        strategy = person.strategy

        pass
        all_nodes = len(list(network.neighbors(node)))
        coops = 0
        for i in network.neighbors(node):
            if network.nodes[i]['personality'].strategy == "C":
                coops += 1
        if float(coops / all_nodes) > 0.8:
            person.new_strategy = "C"
            continue

        mate = 0

        if method == "rd":
            # بازیکن دوم به صورت تصادفی از بین همسایه ها انتخاب میشود
            mate = random.choice(list(network.neighbors(node)))
        elif method == "mu":
            # بازیکن دوم برابر با پرسودترین همسایه قرار میگیرد
            max_util = 0
            for i in network.neighbors(node):
                if network.nodes[i]['personality'].utility > max_util:
                    max_util = network.nodes[i]['personality'].utility
                    mate = i

        second_person = network.nodes[mate]['personality']
        # احتمال اینکه بازیکن اول، استراتژی بازیکن دوم را انتخاب کند
        chance = 0
        # محاسبه تنها در صورتی انجام میشود که استراتژی گره ها متفاوت باشد
        if not person.strategy == second_person.strategy:
            # chance = 90 / 100
            difference = (person.utility - second_person.utility) / (homophily * noise_level)
            # اگر مقداری که در توان e قرار میگیرد از حد مجاز بیشتر باشد، به جای آن بی نهایت قرار میدهیم
            try:
                exponent = math.exp(difference)
            except OverflowError:
                exponent = math.inf
            chance = 1 / 1 + exponent
        if chance > maximum_chance:
            maximum_chance = chance
            strategy = second_person.strategy

        # # احتمال تغییر استراتژی با همه گره های همسایه بررسی میشود
        # for mate in network.neighbors(node):
        #     second_person = network.nodes[mate]['personality']
        #     # احتمال اینکه بازیکن اول، استراتژی بازیکن دوم را انتخاب کند
        #     chance = 0
        #     # محاسبه تنها در صورتی انجام میشود که استراتژی گره ها متفاوت باشد
        #     if not person.strategy == second_person.strategy:
        #         # chance = 90 / 100
        #         difference = (person.utility - second_person.utility) / (homophily * noise_level)
        #         # اگر مقداری که در توان e قرار میگیرد از حد مجاز بیشتر باشد، به جای آن بی نهایت قرار میدهیم
        #         try:
        #             exponent = math.exp(difference)
        #         except OverflowError:
        #             exponent = math.inf
        #         chance = 1 / 1 + exponent
        #     if chance > maximum_chance:
        #         maximum_chance = chance
        #         strategy = second_person.strategy

        # متغیر تصادفی برای اعمال احتمال
        fate = random.randrange(0, 100) / 100
        if maximum_chance > fate:
            # استراتژی مرحله بعد در این فیلد ذخیره میشود تا اثر ناخواسته ای..
            # در فرایند محاسبه استراتژیِ جدیدِ سایر گره ها ایجاد نشود
            person.new_strategy = strategy

    # پس از محاسبه استراتژی جدید تمامی گره ها، این مقدار در متغیر مربوطه قرار میگیرد
    for node in network.nodes():
        person = network.nodes[node]['personality']
        person.strategy = person.new_strategy


