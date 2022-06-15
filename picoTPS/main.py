import time
import rp2
import sys
from machine import Pin, PWM, ADC

# classes we need
class Button:
	def __init__(self,pin):
		self.p = Pin(pin, Pin.IN, Pin.PULL_UP)
	def is_pressed(self):
		return not self.p.value()==1
# constants
MINSRV=1500
MAXSRV=8000
# variables we need
E2E=1024
p=bytearray(E2E)
SB=[0,0,0,0,0,0]
TFN='tps.bin'
WT=[1,2,5]

# hardware pins
DIn=[Pin(6, Pin.IN, Pin.PULL_UP),Pin(7, Pin.IN, Pin.PULL_UP),Pin(8, Pin.IN, Pin.PULL_UP),Pin(9, Pin.IN, Pin.PULL_UP)]
DOut=[Pin(2,Pin.OUT),Pin(3,Pin.OUT),Pin(4,Pin.OUT),Pin(5,Pin.OUT)]
AOut=[PWM(Pin(16)),PWM(Pin(17)),PWM(Pin(20)),PWM(Pin(21))]
AIn=[ADC(Pin(26)),ADC(Pin(27))]
Led = Pin(25,Pin.OUT)
PRG = Button(11)
SEL = Button(10)
TONE = PWM(Pin(18))
def map(a,x1,y1,x2,y2):return int((a-x1)*(y2-x2)/(y1-x1)+x2)
def write(msg): sys.stdout.write(msg)
def writeln(msg): sys.stdout.write(msg);sys.stdout.write('\r\n');
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
def printCheckSum(value):checksum=value&255;checksum=(checksum^255)+1;printHex8(checksum);writeln()
def printHex4(num):write(nibbleToHex(num))
def printHex8(num):write('0x');write(nibbleToHex(num>>4));write(nibbleToHex(num));
def printHex16(num):printHex8(num>>8);printHex8(num)
def printHex16d(num):write("0x%0.4X" % num)
def waitKeyboard():writeln('waiting for command:');writeln('w: write HEX file, r: read file, e: end')

#output 
def doOut(data):
	for i in range(4):DOut[i].value((data&1<<i)>0)
#input
def doIn():
	t=0
	for i in range(4):t=t+(DIn[i].value()<<i)
	return t
#pwm output 4 bit
def analogOut(ch, data):
	AOut[ch].freq(500)
	AOut[ch].duty_u16(data << 12)
#pwm output 8 bit
def analogOutByte(ch, data):
	AOut[ch].freq(500)
	AOut[ch].duty_u16(data << 8)
def servoOut(ch, data):
	AOut[ch].freq(50)
	v = map(data&15,0,15,MINSRV,MAXSRV)
	AOut[ch].duty_u16(v)
def servoOutByte(ch, data):
	AOut[ch].freq(50)
	if data > 180: data=180
	v = map(data,0,180,MINSRV,MAXSRV)
	AOut[ch].duty_u16(v)
def waitPRG():
	while PRG.is_pressed():0
	
#read rc channel
def rcIn(p):
    t=int(machine.time_pulse_us(p,1,40000))
    if t<1000: return 0
    if t>2000: return 255
    return map(t,1000,2000,0,256)

def init():
	for i in range(E2E):p[i]=255
	for i in range(6):SB[i]=0
	for i in range(2):AOut[i].freq(500)
	TONE.duty_u16(int(65536*0.2))

def serialprg(baud):
	return

def save(fn):
	try:os.remove(fn)
	except OSError:writeln(RWE%fn)
	with open(fn,'wb')as mb:mb.write(p)

def load(fn):
	try:
		with open(fn,'rb')as mb:mb.readinto(p)
	except OSError:writeln(RWE%fn)

def sleep(ms):
	time.sleep_ms(ms)

def prg():
	load(TFN);
	doOut(0xf);
	waitPRG();PC=0;PM=True
	
	while PM:
		IN=p[PC]>>4;DT=p[PC]&15;ED=True;NE=True
		while ED:
			while not(PRG.is_pressed()or SEL.is_pressed()):0
			sleep(100)
			if PRG.is_pressed()and SEL.is_pressed():PM=False;break
			if SEL.is_pressed():
				if NE:NE=False;IN=-1
				while SEL.is_pressed():IN=IN+1&15;p[PC]=(IN<<4)+DT;sleep(250)
				continue
			ED=False
		if not PM:break
		waitPRG();ED=True;NE=True
		while ED:
			while not(PRG.is_pressed() or SEL.is_pressed()):0
			sleep(100)
			if PRG.is_pressed()and SEL.is_pressed():PM=False;break
			if SEL.is_pressed():
				if NE:NE=False;DT=-1
				while SEL.is_pressed():DT=DT+1&15;p[PC]=(IN<<4)+DT;sleep(250)
				continue
			ED=False
		waitPRG();sleep(100);PC=PC+1
		if PC>=E2E:break
	save(TFN);sleep(1000)

#checking subroutines
def initSubs():
	for i in range(E2E):
		IN=hi_nib(i)
		if IN==14:
			DT=lo_nib(i)
			if DT>=8 and DT<=13:SB[DT-8]=i

def run():
	Led.value(1)
	time.sleep_ms(200)
	Led.value(0)
	A=0;B=0;C=0;D=0;E=0;F=0;PC=0;PG=0;RT=0;CD=0;DT=0;STP=0
	
	load(TFN)

	initSubs
	
	while True:
		CD=p[PC]>>4;DT=p[PC]&15
#		if uart.any():
#		    c=uart.read(1);ch=chr(c[0])
#		    if ch=='d':DBG=not DBG;dgo(DBG);
#		    if ch=='p':serialprg(BR);reset();
#		if DBG:
#			writeln('-');uart.write('PC: ');printHex16(PC);writeln('');uart.write('INST: ');printHex4(IN);uart.write(', DATA: ');printHex4(DT);writeln('');writeln('Register:');uart.write('A: ');printHex8(A);uart.write(', B: ');printHex8(B);uart.write(', C: ');printHex8(C);writeln('');uart.write('D: ');printHex8(D);uart.write(', E: ');printHex8(E);uart.write(', F: ');printHex8(F);writeln('');uart.write('Page: ');printHex8(PG);uart.write(', Ret: ');printHex16(RT);writeln('')
#			if ST:
#				line=''
#				while not line:line=uart.readline()
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
			if DT>4 and DT<=8:DOut[DT-5].value(A&1)
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
			if DT>4 and DT<=8:A=DIn[DT-5].value()
			if DT>8 and DT<=10:A=AIn[DT-9].read_u16()>>12;
			if DT==11:A=rcIn(AIn[0])>>4
			if DT==12:A=rcIn(AIn[1])>>4
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
			if DT>=4 and DT<=7:s=DIn[DT%4].value()&1==1
			if DT>=8 and DT<=11:s=DIn[DT%4].value()&1==0
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
			if DT==0: A=AIn[0].read_u16()>>8
			if DT==1:A=AIn[1].read_u16()>>8
			if DT==2:A=rcIn(AIn[0])
			if DT==3:A=rcIn(AIn[1])
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
			if DT==13:LED.value(1)
			if DT==14:LED.value(0)
			if DT==15:PC=0;continue
		A=A&255;B=B&255;C=C&255;D=D&255;E=E&255;F=F&255;PC=(PC+1)%E2E
	return

writeln('RPI Pico\r\nrunning pico TPS')
init()
if PRG.is_pressed():prg()
if SEL.is_pressed:serialprg(9600)
run()
writeln('ready')
