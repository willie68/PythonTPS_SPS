import holtek_impl
import sys
import msvcrt
import getopt
from pathlib import Path
import utils
import const


def OutputAll(impl):
    print("-----")
    impl.Register.Print(impl.SPSActive)
    impl.Input.Print()
    print("cmd: 0x{:X} : {}".format(
        impl.cmd, commandSet.GetCommentsForCommand(impl.cmd)))
    impl.Output.Print()


def usage():
    print('tps.py [-h] [--extension] <TPS FILE>')
    print("-h this help text")
    print("--extension activate SPS extensions")


def output(message):
        print(message)


# defining the defaults for this program
extension = False
commandSet = const.CommandSet()

# parsing the command line
try:
    opts, args = getopt.getopt(sys.argv[1:], "he", [
                               "help", "extension"])
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == "-v":
        verbose = True
    elif o in ("-h", "--help"):
        usage()
        sys.exit(0)
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

output("reading file:" + filename)
if not Path(filename).is_file():
    print("file not exists.")
    usage()
    sys.exit(1)

if filename.lower().endswith(".tps"):
    print("reading tps file {}".format(filename))
    program = utils.ReadTPSFile(filename)
elif filename.lower().endswith(".hex"):
    print("reading hex file {}".format(filename))
    program = utils.ReadHEXFile(filename)
elif filename.lower().endswith(".tpsasm"):
    print("reading tpsasm file {}".format(filename))
    program = utils.GetTPSASSFile(filename)
else:
    print("unknown file format.")
    usage()
    sys.exit(1)

output("name:" + impl.getName())
impl.load(bytearray(program))

output("program size:" + str(len(impl.program)))

output("start emulator")
impl.Start()
OutputAll(impl)

output("----- press any key to continue or CTRL+C to stop -----")

while True:
    while impl.HasNext():
        if msvcrt.kbhit():
            key_stroke = msvcrt.getch()
            impl.Execute()
            OutputAll(impl)
            output("----- press any key to continue or CTRL+C to stop -----")
