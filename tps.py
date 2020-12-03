import holtek_impl
import sys
import msvcrt


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


if len(sys.argv) != 2:
    raise ValueError('Please provide the file to process.')

filename = sys.argv[1]

impl = holtek_impl.Holtek(filename)
impl.SPSActive = True

print("reading file:" + filename)
program = ReadTPSFile(filename)

print("name:" + impl.getName())
impl.load(bytearray(program))

print("program size:" + str(len(impl.program)))

print("start emulator")
impl.Start()

print("----- press any key to continue or CTRL+C to stop -----")

while True:
    while impl.HasNext():
        if msvcrt.kbhit():
            key_stroke = msvcrt.getch()
            impl.Execute()
            OutputAll(impl)
            print("----- press any key to continue or CTRL+C to stop -----")

