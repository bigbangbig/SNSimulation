import initialization.initialize as init
import initialization.getting_inputs as gi
# import gui as interface
import plots.main as plots
import games.play as play
import games.update_network as update


# tkinter برای اینترفیس
# py2exe برای ساختن فایل اجرایی برای ویندوز

nodes, edges = gi.main()
cooperatorsPercentage = 30
g = init.go(nodes, edges, cooperatorsPercentage)
count = g.number_of_edges()
print("Edges: " + str(count))

# اطلاعات اولیه گراف را ذخیره میکند. مثل تعداد گره ها
plots.init(g)
plots.save_network_info(g, 0)
# plots.show_network(g)
# بازی به تعداد مشخص شده در رنج بین همه گره ها انجام میشود
for i in range(50):
    play.go(g)
    update.copy_fittest(g)
    plots.save_network_info(g, i + 1)

# رسم نمودار تعداد همکاری کنندگان
plots.plot()
# رسم گراف نهایی
plots.show_network(g)



