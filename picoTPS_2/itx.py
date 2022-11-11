def parsehexline(line):
    cnt = int(len(line) / 2)
    if (len(line) % 2) > 0:
        raise Exception("wrong number of chars")
    data = bytearray(cnt)
    for x in range(cnt):
        dat = int(line[x*2: x*2+2], 16)
        data[x] = dat
    return data

def printbytearray(data):
    for x in data:
        print("%0.2x " % x, end='')    

adr = 0
data = bytearray()
seg = 0
with open('example.hex') as f:
    while ((line := f.readline()) != ""):
        line = line.strip()
        if line.startswith(":") :
            line = line[1:]
            hline = parsehexline(line)
            count = hline[0]
            adr = (hline[1] << 8) + hline[2]
            rectype = hline[3]
            crc = hline[len(hline)-1]
            drc = count + (adr>>8) + (adr & 0xff) + rectype + crc
            if rectype == 0:
                if seg+adr+count > len(data):
                    new = bytearray(seg+adr+count+1)
                    new[:len(data)+1] = data
                    data = new
                for x in range(count):
                    dat = hline[4+x]
                    data[seg+adr+x] = dat
                    drc = drc + dat
                print("data", end ="")
            elif rectype == 1:
                print("eof", end ="")
            elif rectype == 2:
                seg = (hline[4] << 8) +hline[5]
                drc = drc + (seg>>8) + (seg & 0xff)
                seg = seg << 4
                print("ext seg", "0x%0.4x" % seg, end ="")
            else:
                print("start segment: not supported", end ="")
            drc = drc & 0xff
            print(" checksum: ", "%0.2x " % drc, end="")
            if drc == 0 : 
                print("ok")
            else:
                print("not ok")
print("sucess:")
printbytearray(data)