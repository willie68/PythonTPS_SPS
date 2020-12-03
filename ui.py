import holtek_impl
import tkinter as tk


class MainUI(tk.Frame):
    def __init__(self, master=None):
        self.emulator = holtek_impl.Holtek("")
        super().__init__(master)
        self.pack()
        self.master.title = "Python TPS Emulator"
        self.create_widgets()

    def create_widgets(self):
        self.btnSubmit = tk.Button(self, text="Submit", command=self.pressSubmit)
        self.btnSubmit.pack(side="bottom")
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def Output(self, message):
        print("UI:" + message)

    def Go(self):
        self.mainloop()

    def pressSubmit(self):
#        usr = self.app.getEntry("Username")
#        pwd = self.app.getEntry("Password")
        usr = "Willie"
        pwd = "pwd"
        print("User: ", usr, ", Password: ", pwd)
