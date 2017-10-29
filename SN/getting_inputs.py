def get_input(node, edge):
    try:
        node = int(input("How many nodes? "))
        # بررسی اینکه تعداد گره ها کمتر از نباشد
        if node < 2:
            return False, node, edge
        edge = int(input("How many edges? "))
        return True, node, edge
    except Exception:
        print("Exception thrown. Did you enter numbers? this only accepts numbers")
        return False, node, edge


def main():
    nodes = 0
    edges = 0
    res = False
    # تا زمانی که برای تعداد گره ها و یال ها عدد وارد نشده باشد، دریافت مقدار ورودی ادامه می یابد
    while not res:
        res, nodes, edges = get_input(nodes, edges)
    return nodes, edges
