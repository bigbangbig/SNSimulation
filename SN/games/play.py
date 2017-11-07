def prisoners_dilemma(first, second):
    if first == "D" and second == "C":
        return 0, 3
    elif first == "D" and second == "D":
        return 2, 2
    elif first == "C" and second == "D":
        return 3, 0
    else:
        return 1, 1


def go(network):
    for edge in network.edges():
        # در دو سر هر یال، بازیکن ها قرار گرفته اند
        first = network.nodes[edge[0]]
        second = network.nodes[edge[1]]
        my_utility, opponent_utility = prisoners_dilemma(first['personality'].strategy,
                                                         second['personality'].strategy)
        first['personality'].fitness += my_utility
        second['personality'].fitness += opponent_utility

# strategy updates before the next round

