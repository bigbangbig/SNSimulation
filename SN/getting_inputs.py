

def get_input(node, edge):
    try:
        node = int(input("How many nodes? "))
        edge = int(input("How many edges? "))
        return True, node, edge
    except Exception:
        print("Exception thrown. Did you enter numbers? this only accepts numbers")
        return False, node, edge


def main():
    nodes = 0
    edges = 0
    res = False
    while not res:
        res, nodes, edges = get_input(nodes, edges)
        # if res:
        #     break
    return nodes, edges
