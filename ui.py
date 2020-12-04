import holtek_impl
import tkinter as tk


class MainUI(tk.Frame):
    def __init__(self, master=None):
        self.emulator = holtek_impl.Holtek("")
        self.title = "Python TPS Emulator"
        super().__init__(master)
        self.pack()
        self.msg = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.msgLog = tk.Message(self, textvariable = self.msg)
        self.msgLog.grid(row=0, column=1)
        self.msgLog.config(bg='lightgreen', font=('verdana', 12))
        self.btnSubmit = tk.Button(self, text="Submit", command=self.pressSubmit)
        self.btnSubmit.grid(row=1, column=1)
        self.btnQuit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.btnQuit.grid(row=1, column=2)

    def Output(self, message):
        self.msg.set(self.msg.get() + message)
        print("UI:" + self.msg.get())

    def Go(self):
        self.mainloop()

    def pressSubmit(self):
#        usr = self.app.getEntry("Username")
#        pwd = self.app.getEntry("Password")
        usr = "Willie"
        pwd = "pwd"
        self.Output("User: " + usr + ", Password: "+  pwd)
