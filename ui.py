import holtek_impl
import tkinter as tk
import tkinter.filedialog as tf


class MainUI(tk.Frame):
    def NewFile(self):
        print("New File!")

    def OpenFile(self):
        name = tf.askopenfilename()
        print(name)

    def About(self):
        print("This is a simple example of a menu")

    def __init__(self):
        self.root = tk.Tk()
        self.emulator = holtek_impl.Holtek("")
        self.title = "Python TPS Emulator"
        super().__init__(self.root)
        self.master.geometry("300x300")
        self.menu = tk.Menu(self)
        self.master.config(menu=self.menu)
        filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.NewFile)
        filemenu.add_command(label="Open...", command=self.OpenFile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)

        helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.About)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        h = tk.Scrollbar(self.root, orient='horizontal')
        h.pack(side=tk.BOTTOM, fill=tk.X)
        v = tk.Scrollbar(self.root, orient='vertical')
        v.pack(side=tk.RIGHT, fill=tk.Y)
        self.msgLog = tk.Text(self.root, width=15, height=10, wrap=tk.NONE,
                              xscrollcommand=h.set,
                              yscrollcommand=v.set)
        self.msgLog.insert(tk.INSERT, "Hallo")            
        self.msgLog.pack(side=tk.TOP, fill=tk.BOTH)
        self.msgLog.config(bg='lightgreen', font=('verdana', 12))
        h.config(command=self.msgLog.xview)
        v.config(command=self.msgLog.yview)

        self.frame = tk.Frame(self.root)

        self.btnSubmit = tk.Button(
            self.frame, text="Submit", command=self.pressSubmit)
        self.btnSubmit.grid(row=1, column=1)
        self.btnQuit = tk.Button(self.frame, text="QUIT", fg="red",
                                 command=self.master.destroy)
        self.btnQuit.grid(row=1, column=2)
        self.frame.pack(side=tk.BOTTOM, fill=tk.X)

    def Output(self, message):
        self.msgLog.insert(tk.INSERT, message)
        print("UI:" + message)

    def Go(self):
        self.mainloop()

    def pressSubmit(self):
        #        usr = self.app.getEntry("Username")
        #        pwd = self.app.getEntry("Password")
        usr = "Willie"
        pwd = "pwd"
        self.Output("User: " + usr + ", Password: " + pwd)
