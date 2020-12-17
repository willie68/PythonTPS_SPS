import tkinter as tk
import Emulator
import sys
import msvcrt
import getopt
import ui
from pathlib import Path
import utils
import const
import os


def OutputAll(impl):
    print("-----")
    impl.Register.Print(impl.SPSActive)
    impl.Input.Print()
    print("cmd: 0x{:X} : {}".format(
        impl.cmd, commandSet.GetCommentsForCommand(impl.cmd)))
    impl.Output.Print()

def usage():
    print('tpsasm.py [-h] [--extension|-e] <TPS Assembler file> [intel hex file]')
    print('assembles the source file into a intel hex format used by the tps.')
    print("-h this help text")
    print("--extension activates the sps extensions")


def output(message):
    print(message)


# defining the defaults for this program
extension = True
commandSet = const.CommandSet()

# parsing the command line
try:
    opts, args = getopt.getopt(sys.argv[1:], "he", [
                               "help",  "extension"])
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
destname = ""
if len(args) > 1:
    destname = args[1]
else:
    destname = os.path.splitext(filename)[0] + ".hex" 

output("reading file:" + filename)
if not Path(filename).is_file():
    print("file not exists.")
    usage()
    sys.exit(1)

if filename.lower().endswith(".tpsasm"):
    print("reading tpsasm file {}".format(filename))
    program = utils.GetTPSASSFile(filename)
    utils.WritingIntelHexFile(program, destname)
else:
    print("unknown file format.")
    usage()
    sys.exit(1)

print("program exit")