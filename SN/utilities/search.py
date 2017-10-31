def find_node_by_id(_id, network):
    nodes = network.nodes()
    for x in nodes:
        if x.id == _id:
            break
    else:
        x = None
    return x
