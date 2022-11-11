import time
import sys
import os
import errno
import board
import usb_cdc
import microcontroller
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
from pwmio import PWMOut

# classes we need
class Button:
	def __init__(self,pin):
		self.p = DigitalInOut(pin)
		self.p.direction = Direction.INPUT
		self.p.pull = Pull.UP
	def is_pressed(self):
		return not self.p.value
# constants
MINSRV=1500
MAXSRV=8000
CR=bytearray('\r\n')

BLINK_DELAY=500
SHOW_DELAY=1000
KEY_DELAY=250
ADDR_LOOP=50
DEBOUNCE=100
PRG_ADDRESS=1
PRG_COMMAND=2
PRG_DATA=3
prgMode=0

DEMO_PRG = [0x4F, 0x59, 0x1F, 0x29, 0x10, 0x29, 0x5A, 0x40,
            0x59, 0x64, 0x54, 0x29, 0x4F, 0x59, 0x10, 0xCD,
            0x11, 0x28, 0xCC, 0x18, 0x28, 0x4F, 0x59, 0x5A,
            0x72, 0x26, 0xC0, 0x35, 0x80, 0x90, 0xFF]

# variables we need
E2E=1024
p=bytearray(E2E)
PN='raspberry pi pico'
SB=[0,0,0,0,0,0]
TFN='tps.bin' #filename of the tps bin file
WT=[1,2,5]
DBG = False # debug mode
ST = False # single step

# hardware pins
DIn=[DigitalInOut(board.GP6),DigitalInOut(board.GP7),DigitalInOut(board.GP8),DigitalInOut(board.GP9)]
DOut=[DigitalInOut(board.GP2),DigitalInOut(board.GP3),DigitalInOut(board.GP4),DigitalInOut(board.GP5)]
AOut=[PWMOut(board.GP16, frequency=50, duty_cycle=0),PWMOut(board.GP17, frequency=50, duty_cycle=0),PWMOut(board.GP20, frequency=50, duty_cycle=0),PWMOut(board.GP21, frequency=50, duty_cycle=0)]
AIn=[AnalogIn(board.GP26),AnalogIn(board.GP27)]
#RCIn=[Pin(14), Pin(15)]
Led = DigitalInOut(board.LED)
Led.direction = Direction.OUTPUT
PRG = Button(board.GP11)
SEL = Button(board.GP10)
#TONE = PWM(Pin(18))
#Debug serial
serial = usb_cdc.data
def map(a,x1,y1,x2,y2):return int((a-x1)*(y2-x2)/(y1-x1)+x2)
def write(msg): serial.write(bytearray(msg))
def writeln(msg):
    write(msg);
    serial.write(CR);
def hi_nib(pb):return p[pb]>>4&15
def lo_nib(pb):return p[pb]&15
def get_nib(pb,nib):
	if nib:return p[pb]&15
	else:return p[pb]>>4&15
def set_nib(pb,nib,v):
	if nib:p[pb]=p[pb]&240|v
	else:p[pb]=v<<4|p[pb]&15
def hexToByte(c):
	if c>='0'and c<='9':return ord(c)-ord('0')
	if c>='A'and c<='F':return ord(c)-ord('A')+10
def nibbleToHex(value):
	c=value&15
	if c>=0 and c<=9:return chr(c+ord('0'))
	if c>=10 and c<=15:return chr(c-10+ord('A'))
def printCheckSum(value):checksum=value&255;checksum=(checksum^255)+1;printHex8(checksum);writeln('')
def printHex4(num):write(nibbleToHex(num))
def printHex8(num):write(nibbleToHex(num>>4));write(nibbleToHex(num));
def printHex16(num):printHex8(num>>8);printHex8(num)
def printHex16d(num):write("%0.4X" % num)
def writeProgramSerial():
	writeln('program data:');checksum=0
	for pc in range(E2E):
		value=p[pc]
		if pc%8==0:
			if pc>0:printCheckSum(checksum)
			checksum=0;write(':08');checksum+=8;printHex16(pc);checksum+=pc>>8;checksum+=pc&255;write('00')
		printHex8(value);checksum+=value
	printCheckSum(checksum);writeln(':00000001FF')
def dgo(d):
	if d:writeln('dbg on')
	else:writeln('dbg off')
def waitKeyboard():writeln('waiting for command:');writeln('w: write HEX file, r: read file, e: end')
def getNextChar():
	while serial.in_waiting == 0:sleep(10)
	c=serial.read(1);return chr(c[0])
#output 
def doOut(data):
	for i in range(4):DOut[i].value = (data&1<<i)>0
#input
def doIn():
	t=0
	for i in range(4):t=t+(DIn[i].value << i)
	return t
#pwm output 4 bit
def analogOut(ch, data):
	#AOut[ch].frequency=500
	AOut[ch].duty_cycle=data << 12
#pwm output 8 bit
def analogOutByte(ch, data):
	#AOut[ch].frequency=500
	AOut[ch].duty_cycle=data << 8
def servoOut(ch, data):
	#AOut[ch].frequency=50
	v = map(data&15,0,15,MINSRV,MAXSRV)
	AOut[ch].duty_cycle=v
def servoOutByte(ch, data):
	#AOut[ch].freq(50)
	if data > 180: data=180
	v = map(data,0,180,MINSRV,MAXSRV)
	AOut[ch].duty_cycle=v
def waitPRG():
	while PRG.is_pressed():0
#read rc channel
def rcIn(p):
    t=int(machine.time_pulse_us(RCIn[p],1,40000))
    if t<1000: return 0
    if t>2000: return 255
    return map(t,1000,2000,0,256)

def init():
	for i in DIn:
		i.direction=Direction.INPUT
		i.pull=Pull.UP

	for o in DOut: o.direction = Direction.OUTPUT

	for i in range(E2E):p[i]=255
	for i in range(6):SB[i]=0
	#for i in range(2):AOut[i].freq(500)
	#TONE.duty_u16(int(65536*0.2))
	try:
		f = open(TFN)
		f.close()
	except OSError:
		for i in range(len(DEMO_PRG)):p[i]=DEMO_PRG[i]
		save(TFN)

def serialprg():
	eOfp=False;write(CR);writeln(PN);waitKeyboard()
	while not eOfp:
		while serial.in_waiting>0:
			c=serial.read(1);ch=chr(c[0])
			if ch=='w':
				writeln('ready');eOfF=False;data=bytearray(32)
				while True:
					for i in range(8):data[i]=255
					while True:
						c=getNextChar()
						if c==':':break
					c=getNextChar();count=hexToByte(c)<<4;c=getNextChar();count+=hexToByte(c);crc=count;c=getNextChar();readAddress=hexToByte(c)<<12;c=getNextChar();readAddress+=hexToByte(c)<<8;c=getNextChar();readAddress+=hexToByte(c)<<4;c=getNextChar();readAddress+=hexToByte(c);crc+=readAddress>>8;crc+=readAddress&255;c=getNextChar();type=hexToByte(c)<<4;c=getNextChar();type+=hexToByte(c);crc+=type
					if type==1:eOfF=True
					for x in range(count):c=getNextChar();value=hexToByte(c)<<4;c=getNextChar();value+=hexToByte(c);data[x]=value;crc+=value
					c=getNextChar();readcrc=hexToByte(c)<<4;c=getNextChar();readcrc+=hexToByte(c);crc+=readcrc;value=crc&255
					if value==0:
						write('ok')
						for x in range(count):p[readAddress+x]=data[x]
					else:writeln(', CRC Error');eOfF=True
					writeln('')
					if eOfF:break
				writeln('endOfFile');save(TFN)
			elif ch=='r':load(TFN);writeProgramSerial()
			elif ch=='e':writeln('end');eOfp=True
			else:waitKeyboard()
	return

def save(fn):
	try: os.remove(fn)
	except OSError as exc:
		print("error on file: \r\n", exc)
	with open(fn,'wb')as mb:mb.write(p)

def load(fn):
	try:
		with open(fn,'rb')as mb:mb.readinto(p)
	except OSError as exc:
		print("error opnening file: ", errno.errorcode[exc.errno], '\r\n')

def reset():
	writeln('resetting')
	microcontroller.reset()

def sleep(ms):
	time.sleep(ms/1000)

def blinkAll():
	blinkNull();
	doOut(0x0F);
	sleep(BLINK_DELAY);

def blinkD1():
	blinkNull();
	doOut(0x01);
	sleep(BLINK_DELAY);
	blinkNull();

def blinkD2():
	blinkNull();
	doOut(0x02);
	sleep(BLINK_DELAY);
	blinkNull();

def blinkD3():
	blinkNull();
	doOut(0x04);
	sleep(BLINK_DELAY);
	blinkNull();

def blinkD4():
	blinkNull();
	doOut(0x08);
	sleep(BLINK_DELAY);
	blinkNull();

def blinkNull():
	doOut(0);
	sleep(BLINK_DELAY);

def doAddr(value):
  for i in range(ADDR_LOOP):
    doOut(value);
    sleep(19);
    doOut(0x0F);
    sleep(1);

def prg():
	writeln('start programming');
	load(TFN);
	doOut(0x08);
	waitPRG();
	blinkAll();
	
	prgMode = PRG_ADDRESS;
	
	PC=0;
	programming=True;
	changed=False;
	
	while programming:
		write('PC:');
		printHex16d(PC);
		writeln('');
		blinkD1();
		doAddr(PC);
		
		blinkD2();
		# HiNibble Adresse anzeigen
		data = (PC & 0xf0) >> 4;
		# Adresse anzeigen
		doAddr(data);
		# delay(SHOW_DELAY);
		
		Eebyte = p[PC];
		data = Eebyte & 15;
		com = Eebyte >> 4;
		write('C: 0x');printHex4(com);
		write(', D: 0x');printHex4(data);
		writeln('');
		blinkD3();
		prgMode = PRG_COMMAND;
		doOut(com); #show command

		while True:
			if (SEL.is_pressed() and PRG.is_pressed()): programming = False; break;
			if (SEL.is_pressed()):
				sleep(KEY_DELAY);
				com += 1;
				com = com & 0x0F;
				doOut(com);
			if PRG.is_pressed():
				break;
		
		if not programming: break; #vorzeitiger Abbruch
		
		blinkD4();
		prgMode = PRG_DATA;
		doOut(data); #show data

		while True:
			if (SEL.is_pressed() and PRG.is_pressed()): programming = False; break;
			if (SEL.is_pressed()):
				sleep(KEY_DELAY);
				data += 1;
				data = data & 0x0F;
				doOut(data);
			if (PRG.is_pressed()):
				break; # S2 = 1
		
		if (programming):
			writeln('setting new value');
			newValue = (com << 4) + data;
			if (newValue != Eebyte):
				p[PC] = newValue;
				blinkAll();
				changed = True;
		PC += 1;
	
	if (changed):
		writeln('saving file');
		save(TFN);
	sleep(1000);

#checking subroutines
def initSubs():
	for i in range(E2E):
		IN=hi_nib(i)
		if IN==14:
			DT=lo_nib(i)
			if DT>=8 and DT<=13:SB[DT-8]=i

def run():
	Led.value = 1
	time.sleep(0.2)
	Led.value = 0
	A=0;B=0;C=0;D=0;E=0;F=0;PC=0;PG=0;RT=0;CD=0;DT=0;STP=0
	DBG=False
	
	load(TFN)

	initSubs
	
	while True:
		CD=p[PC]>>4;DT=p[PC]&15
		if serial.in_waiting > 0:
		    c=serial.read(1);ch=chr(c[0])
		    if ch=='d':DBG=not DBG;dgo(DBG);
		    if ch=='p':serialprg();reset();
		if DBG:
			writeln('-')
			write('PC: ');printHex16(PC);writeln('')
			write('INST: ');printHex4(CD);write(', DATA: ');printHex4(DT);writeln('')
			writeln('Register:');write('A: ');printHex8(A);write(', B: ');printHex8(B);write(', C: ');printHex8(C);writeln('')
			write('D: ');printHex8(D);write(', E: ');printHex8(E);write(', F: ');printHex8(F);writeln('')
			write('Page: ');printHex8(PG);write(', Ret: ');printHex16(RT);writeln('')
			if ST:
				line=''
				while not line:line=uart.readline()
		#DOut
		if CD==1: doOut(DT)
		#Sleep
		if CD==2:
			if DT==14:slp=30000
			if DT==15:slp=60000
			else:slp=10**(DT//3)*WT[DT%3]
			sleep(slp)
		#Jumpback
		if CD==3:PC=PC-DT-1
		# A=#
		if CD==4:A=DT
		#x=A
		if CD==5:
			if DT==0:tmp=A;A=B;B=tmp
			if DT==1:B=A
			if DT==2:C=A
			if DT==3:D=A
			if DT==4:doOut(A)
			if DT>4 and DT<=8:DOut[DT-5].value = A&1
			if DT>8 and DT<=10:analogOut(DT-9, A)
			if DT>10 and DT<=12:servoOut(DT-11, A)
			if DT==13:E=A
			if DT==14:F=A
			if DT==15:
				STK[STP]=A;STP+=1
				if STP>15:STP=15
		#A=x
		if CD==6:
			if DT==1:A=B
			if DT==2:A=C
			if DT==3:A=D
			if DT==4:A=doIn()
			if DT>4 and DT<=8:A=DIn[DT-5].value
			if DT>8 and DT<=10:A=AIn[DT-9].value>>12;
			if DT==11:A=rcIn(0)>>4
			if DT==12:A=rcIn(1)>>4
			if DT==13:A=E
			if DT==14:A=F
			if DT==15:
				STP-=1
				if STP<0:STP=0
				A=STK[STP]
		if CD==7:
			if DT==1:A=A+1
			if DT==2:A=A-1
			if DT==3:A=A+B
			if DT==4:A=A-B
			if DT==5:A=A*B
			if DT==6:
				if B:A=A//B
			if DT==7:A=A&B
			if DT==8:A=A|B
			if DT==9:A=A^B
			if DT==10:A=~ A
			if DT==11:A=A%B
			if DT==12:A=A+16*B
			if DT==13:A=B-A
			if DT==14:A=A>>1
			if DT==15:A=A<<1
		if CD==8:PG=DT*16
		if CD==9:PC=PG+DT;continue
		if CD==10:
			if C>0:C=C-1;PC=PG+DT;continue
		if CD==11:
			if D>0:D=D-1;PC=PG+DT;continue
		if CD==12:
			s=False
			if DT==0:s=A==0
			if DT==1:s=A>B
			if DT==2:s=A<B
			if DT==3:s=A==B
			if DT>=4 and DT<=7:s=DIn[DT%4].value &1==1
			if DT>=8 and DT<=11:s=DIn[DT%4].value &1==0
			if DT==12:s=PRG.is_pressed()
			if DT==13:s=SEL.is_pressed()
			if DT==14:s=not PRG.is_pressed()
			if DT==15:s=not SEL.is_pressed()
			if s:PC=PC+1
		if CD==13:RT=PC+1;PC=PG+DT;continue
		if CD==14:
			if DT==0:PC=RT-1
			if DT>=1 and DT<=6:RT=PC;PC=SB[DT-1];continue
			if DT==15:reset()
		if CD==15:
			if DT==0: A=AIn[0].value>>8
			if DT==1:A=AIn[1].value>>8
			if DT==2:A=rcIn(0)
			if DT==3:A=rcIn(1)
			if DT==4:analogOutByte(0, A)
			if DT==5:analogOutByte(1, A)
			if DT==6:servoOutByte(0, A)
			if DT==7:servoOutByte(1, A)
			if DT==8:
				if A==0:TONE.duty_u16(0)
				if A>0:f=440*2**((A-69)/12);TONE.duty_u16(int(65536*0.2));TONE.freq(int(f))
			if DT==9:analogOutByte(2, A)
			if DT==10:analogOutByte(3, A)
			if DT==11:servoOutByte(2, A)
			if DT==12:servoOutByte(3, A)
			if DT==13:Led.value=1
			if DT==14:Led.value=0
			if DT==15:PC=0;continue
		A=A&255;B=B&255;C=C&255;D=D&255;E=E&255;F=F&255;PC=(PC+1)%E2E
	return

writeln('RPI Pico\r\nrunning pico TPS')
init()
if PRG.is_pressed():prg()
if SEL.is_pressed():serialprg()
writeln('running program')
run()
writeln('ready')
