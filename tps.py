import holtek_impl
import sys


def OutputAll(impl):
    impl.Input.Print()
    impl.Output.Print()
    impl.Register.Print(impl.SPSActive)
    print("cmd: 0x{:X}".format(impl.cmd))


def ReadTPSFile(filename):
    program = []
    f = open("blink.tps", "r")
    for x in f:
        if not x.startswith('#'):
            li = x.split(",")
            cmd = int("0x" + li[1] + li[2], 16)
            print(cmd)
            program.append(cmd)
    f.close()
    return program


if len(sys.argv) != 2:
    raise ValueError('Please provide the file to process.')

filename = sys.argv[1]

impl = holtek_impl.Holtek("blink.tps")
impl.SPSActive = True

program = ReadTPSFile("Blink.tps")
print(impl.getName())
print(impl.program)

impl.load(bytearray(program))

print(impl.program)
OutputAll(impl)

impl.Start()

while impl.HasNext():
    print("-----")
    impl.Execute()
    OutputAll(impl)
