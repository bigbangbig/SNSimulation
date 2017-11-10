import initialization.initialize as init
import plots.main as plots
import games.play as play
import games.update_network as update

#  اطلاعات اولیه گراف را ذخیره میکند. مثل تعداد گره ها
G = init.go(500, 30)
plots.init(G)
plots.save_network_info(G, 0)

# # بازی به تعداد مشخص شده در range بین همه گره ها انجام میشود
for i in range(200):
    play.go(G)
    # update.copy_fittest(G)
    update.conditional_update(G)
    plots.save_network_info(G, i + 1)

plots.show_results(G)






