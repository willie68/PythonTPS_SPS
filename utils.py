from intelhex import IntelHex
import requests
import sys
import io

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
    print(program)
    return program

def GetTPSASSFile(filename):
    program = []
    f = open(filename, "r")
    data = f.read()
    f.close()
    print("----- source -----")
    print(data)
    url = 'http://wkla.no-ip.biz/tps/assembler/ass.php'
    myobj = {'name': 'blink.tpsasm', 'dest': 'ARDUINOSPS', 'output': 'INTELHEX', "source": data }

    x = requests.post(url, data = myobj)
    if x.status_code == 200:
        inteltext = x.text
        print("----- hex -----")
        print(inteltext)
        ih = IntelHex()
        ih.loadhex(io.StringIO(inteltext))
        program = ih.tobinarray()
    else:
        print("----- error -----")
        print("code: {} \r\n {}".format(x.status_code, x.text))
        x.raise_for_status()
    print(program)
    return program

def WritingIntelHexFile(program, destname):
    ih = IntelHex()
    ih.frombytes(program)
    ih.write_hex_file(destname)