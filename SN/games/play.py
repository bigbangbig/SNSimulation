def prisoners_dilemma(first, second):
    if first == "D" and second == "C":
        return 4, 1
    elif first == "D" and second == "D":
        return 2, 2
    elif first == "C" and second == "D":
        return 1, 4
    else:
        return 3, 3


def snow_drift(first, second):
    if first == "D" and second == "C":
        return 4, 2
    elif first == "D" and second == "D":
        return 1, 1
    elif first == "C" and second == "D":
        return 2, 4
    else:
        return 3, 3


def go(network, game):
    # عایدی گره ها در این مرحله صفر میشود تا عایدی آنها مختص به دست کنونی از بازی باشد
    # برخلاف عایدی که مختص به هر دست از بازیست، برازندگی در طول زمان افزایش می یابد و برابر با مجموع..
    # ..عایدی های هر گره در تمام دست های بازیست
    for node in network.nodes():
        network.nodes[node]['personality'].utility = 0

    for edge in network.edges():
        # در دو سر هر یال، بازیکن ها قرار گرفته اند
        first = network.nodes[edge[0]]
        second = network.nodes[edge[1]]
        my_utility = 0
        opponent_utility = 0
        if game == 'pd':
            my_utility, opponent_utility = prisoners_dilemma(first['personality'].strategy,
                                                             second['personality'].strategy)
        elif game == 'sd':
            my_utility, opponent_utility = snow_drift(first['personality'].strategy,
                                                      second['personality'].strategy)

        first['personality'].fitness += my_utility
        first['personality'].utility += my_utility
        second['personality'].fitness += opponent_utility
        second['personality'].utility += opponent_utility


