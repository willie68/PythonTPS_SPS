import Emulator
import tkinter as tk
import tkinter.filedialog as tf
import const

class TextScrollCombo(tk.Frame):
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    # ensure a consistent GUI size
        self.grid_propagate(False)
    # implement stretchability
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # create a Text widget
        self.txt = tk.Text(self)
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    # create a Scrollbar and associate it with txt
        scrollb = tk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

class MainUI(tk.Frame):
    def NewFile(self):
        print("New File!")

    def OpenFile(self):
        name = tf.askopenfilename()
        print(name)

    def About(self):
        print("This is a simple example of a menu")

    def __init__(self):
        self.commandSet = const.CommandSet()
        self.root = tk.Tk()
        self.emulator = Emulator.TPSSPSEmulator("")
        super().__init__(self.root)
        self.master.geometry("600x300")
        self.createMenu()
        self.pack()
        self.root.title("Python TPS Emulator")
        self.create_widgets()

    def createMenu(self):
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

    def create_widgets(self):
        self.createToolbar()
        self.createMessageSection()
        self.createSourceSection()
#        self.createInputSection()

    def createInputSection(self):
        self.group = tk.LabelFrame(self.root, text='Verbindung')
        self.group.config(width= 80)
        label = tk.Label(self.group, bg='black', width=80)
        label.pack()
        self.group.pack(side=tk.RIGHT)

    def createSourceSection(self):
        self.source = TextScrollCombo(self.root)
        self.source.pack(fill="both") #, expand=True)
        self.source.config(width=600, height=600)
        self.source.txt.config(font=("consolas", 12), undo=True, wrap='word')
        self.source.txt.config(borderwidth=3, relief="sunken")
        self.source.txt.insert(tk.INSERT, "Source\r\n")

    def createMessageSection(self):
        self.msgLog = TextScrollCombo(self.root)
        self.msgLog.pack(fill="x", expand=True)
        self.msgLog.config(width=600, height=150)
        self.msgLog.txt.config(font=("consolas", 10), bg='lightgray', undo=True, wrap='none')
        self.msgLog.txt.config(borderwidth=1)
        self.msgLog.txt.insert(tk.INSERT, "Messages\r\n")

#       self.msgLog = tk.Text(self.root, width=15, height=10, wrap=tk.NONE)
#        h = tk.Scrollbar(self.msgLog, orient='horizontal')
#        h.pack(side=tk.BOTTOM, fill=tk.X)
#        v = tk.Scrollbar(self.msgLog, orient='vertical')
#        v.pack(side=tk.RIGHT, fill=tk.Y)
#        self.msgLog['yscrollcommand'] = v.set
#        self.msgLog['xscrollcommand'] = h.set
#        self.msgLog.pack(side=tk.BOTTOM, fill=tk.BOTH)
#        self.msgLog.config(bg='lightgreen', font=('verdana', 12))
#        h.config(command=self.msgLog.xview)
#        v.config(command=self.msgLog.yview)

    def createToolbar(self):
        self.frame = tk.Frame(self.root)
        self.btnSubmit = tk.Button(
            self.frame, text="Submit", command=self.pressSubmit)
        self.btnSubmit.grid(row=1, column=1)
        self.btnQuit = tk.Button(self.frame, text="QUIT", fg="red",
                                 command=self.master.destroy)
        self.btnQuit.grid(row=1, column=2)
        self.frame.pack(side=tk.TOP, fill=tk.X)

    def insertProgram(self, program):
        for cmd in program:
            self.source.txt.insert(tk.INSERT, "cmd: 0x{:X} : {}\r\n".format(
        cmd, self.commandSet.GetCommentsForCommand(cmd)) )
            self.msgLog.txt.insert(tk.INSERT, "cmd: 0x{:X} : {}\r\n".format(
        cmd, self.commandSet.GetCommentsForCommand(cmd)) )

    def Output(self, message):
        self.msgLog.txt.insert(tk.INSERT, message + "\r\n")
        print("UI:" + message)

    def Go(self):
        self.mainloop()

    def pressSubmit(self):
        #        usr = self.app.getEntry("Username")
        #        pwd = self.app.getEntry("Password")
        usr = "Willie"
        pwd = "pwd"
        self.Output("User: " + usr + ", Password: " + pwd)
