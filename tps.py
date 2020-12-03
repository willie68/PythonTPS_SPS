import tkinter as tk
import holtek_impl
import sys
import msvcrt
import getopt
import ui

def OutputAll(impl):
    impl.Input.Print()
    impl.Output.Print()
    impl.Register.Print(impl.SPSActive)
    print("cmd: 0x{:X}".format(impl.cmd))


def ReadTPSFile(filename):
    program = []
    f = open(filename, "r")
    for x in f:
        if not x.startswith('#'):
            li = x.split(",")
            cmd = int("0x" + li[1] + li[2], 16)
            program.append(cmd)
    f.close()
    return program

def usage():
    print('tps.py [-h] [--ui] [--extension] <TPS FILE>')
    print("-h this help text")
    print("--ui create graphical interface")
    print("--extension activate SPS extensions")

def output(message):
    if isinstance(window, ui.MainUI):
        window.Output(message)
    else:
        print(message)

# defining the defaults for this program
extension = False
displayGUI = False

#parsing the command line
try:
    opts, args = getopt.getopt(sys.argv[1:],"hue",["help", "ui", "extension"])
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == "-v":
        verbose = True
    elif o in ("-h", "--help"):
        usage()
        sys.exit(0)
    elif o in ("-u", "--ui"):
        displayGUI = True
    elif o in ("-e", "--extension"):
        extension = True
    else:
        assert False, "unhandled option"

if len(args) == 0:
    usage()
    sys.exit(2)

filename = args[0]

# initialising the emulator core
impl = holtek_impl.Holtek(filename)
impl.SPSActive = extension
window = 0

output("reading file:" + filename)
program = ReadTPSFile(filename)

output("name:" + impl.getName())
impl.load(bytearray(program))

output("program size:" + str(len(impl.program)))

#wrapping up the ui
if displayGUI:
    window = ui.MainUI()
    window.emulator = impl
    window.Go()
else:
    output("start emulator")
    impl.Start()

    output("----- press any key to continue or CTRL+C to stop -----")

    while True:
        while impl.HasNext():
            if msvcrt.kbhit():
                key_stroke = msvcrt.getch()
                impl.Execute()
                OutputAll(impl)
                output("----- press any key to continue or CTRL+C to stop -----")

