import tkinter as tk
import holtek_impl
import sys
import msvcrt
import getopt
import ui
from pathlib import Path
import utils
import const


def OutputAll(impl):
    impl.Input.Print()
    print("cmd: 0x{:X} : {}".format(
        impl.cmd, commandSet.GetCommentsForCommand(impl.cmd)))
    impl.Output.Print()
    impl.Register.Print(impl.SPSActive)


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
commandSet = const.CommandSet()

# parsing the command line
try:
    opts, args = getopt.getopt(sys.argv[1:], "hue", [
                               "help", "ui", "extension"])
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
if not Path(filename).is_file():
    print("file not exists.")
    usage()
    sys.exit(1)

if filename.lower().endswith(".tps"):
    program = utils.ReadTPSFile(filename)
elif filename.lower().endswith(".hex"):
    program = utils.ReadHEXFile(filename)
else:
    print("unknown file format.")
    usage()
    sys.exit(1)

output("name:" + impl.getName())
impl.load(bytearray(program))

output("program size:" + str(len(impl.program)))

# wrapping up the ui
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
