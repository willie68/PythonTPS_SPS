from intelhex import IntelHex

def constrain(x, a, b):
    if x < a: 
        return a
    if x > b:
        return b
    return x

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

def ReadHEXFile(filename):
    program = []
    ih = IntelHex(filename)
    program = ih.tobinarray()
    return program