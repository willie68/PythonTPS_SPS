# import the library
from appJar import gui

def press(button):
    if button == "Cancel":
        app.stop()
    else:
        usr = app.getEntry("Username")
        pwd = app.getEntry("Password")
        print("User: ", usr, ", Password: ", pwd)


# create a GUI variable called app
app = gui()

app.addLabel("title", "Welcome to appJar")
app.addLabelEntry("Username")
app.addLabelSecretEntry("Pwd")
app.addButtons(["Submit", "Cancel"], press)
app.go()
