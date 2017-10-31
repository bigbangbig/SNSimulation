from appJar import gui

title = "SN"
app = gui(title, "400x200")


def press(button):
    if button == "Cancel":
        app.stop()
    else:
        print("Hi")


def init():
    app.addLabel(title, "شبیه سازی شبکه")
    app.setLabelBg(title, "red")
    return app


def create_and_display():
    init()
    app.addButtons(["Submit", "Cancel"], press)
    app.go()


create_and_display()