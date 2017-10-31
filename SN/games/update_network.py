import utilities.search as ut


# از بین همسایگان، استراتژی برازنده ترین آنها به عنوان استراتژی دور بعد انتخاب میشود
def copy_fittest(network):
    for node in network.nodes():
        # update nodes
        maximum_fitness = 0
        fittest_mate = 0
        for mate in network.neighbors(node):
            if mate.fitness > maximum_fitness:
                maximum_fitness = mate.fitness
                fittest_mate = mate.id
        # استراتژی برازنده ترین همسایه انتخاب می شود
        node.new_strategy = ut.find_node_by_id(fittest_mate, network).strategy

    # استراتژی های انتخاب شده به عنوان استراتژی مرحله بعد ثبت میشوند
    for node in network.nodes():
        node.strategy = node.new_strategy
