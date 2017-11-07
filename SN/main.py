import initialization.initialize as init
import plots.main as plots
import games.play as play
import games.update_network as update
import networkx as nx


# nodes, edges = gi.main()
# cooperatorsPercentage = 30
# g = init.go(nodes, edges, cooperatorsPercentage)
# count = g.number_of_edges()
# print("Edges: " + str(count))
#
# # اطلاعات اولیه گراف را ذخیره میکند. مثل تعداد گره ها
# plots.init(g)
# # plots.show_network(g)

# # رسم نمودار تعداد همکاری کنندگان
# plots.plot()
# # رسم گراف نهایی
# plots.show_network(g)

G = init.go(101, 50)
plots.init(G)
plots.save_network_info(G, 0)
# # بازی به تعداد مشخص شده در رنج بین همه گره ها انجام میشود
for i in range(50):
    play.go(G)
    update.copy_fittest(G)
    plots.save_network_info(G, i + 1)
plots.draw(G)






