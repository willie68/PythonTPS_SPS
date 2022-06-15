RWE='rw error %s'
from microbit import *
import machine,music,gc,os
gc.collect()
BR=115200
BT=True
BF=False
DBG=BT
ST=BF
PN='micro:bit v2'
CR='\r\n'
TFN='tps.bin'
E2E=1024
p=bytearray(E2E)
STK=bytearray(16)
STP=0
SEL=button_a
PRG=button_b
music_note=['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']
SB=[0,0,0,0,0,0]
WT=[1,2,5]
DI=[pin13,pin14,pin15,pin16]
DO=[pin0,pin1,pin2,pin12]
AO=[pin8,pin9]
AI=[pin3,pin4]
images={1:Image.HEART,2:Image.HAPPY,3:Image.SMILE,4:Image.SAD,5:Image.CONFUSED,6:Image.ANGRY,7:Image.ASLEEP,8:Image.SURPRISED,9:Image.SILLY,10:Image.FABULOUS,11:Image.MEH,12:Image.YES,13:Image.NO,14:Image.CLOCK1,15:Image.CLOCK2,16:Image.CLOCK3,17:Image.CLOCK4,18:Image.CLOCK5,19:Image.CLOCK6,20:Image.CLOCK7,21:Image.CLOCK8,22:Image.CLOCK9,23:Image.CLOCK10,24:Image.CLOCK11,25:Image.CLOCK12,26:Image.ARROW_N,27:Image.ARROW_NE,28:Image.ARROW_E,29:Image.ARROW_SE,30:Image.ARROW_S,31:Image.ARROW_SW,32:Image.ARROW_W,33:Image.ARROW_NW,34:Image.TRIANGLE,35:Image.TRIANGLE_LEFT,36:Image.CHESSBOARD,37:Image.DIAMOND,38:Image.DIAMOND_SMALL,39:Image.SQUARE,40:Image.SQUARE_SMALL,41:Image.RABBIT,42:Image.COW,43:Image.MUSIC_CROTCHET,44:Image.MUSIC_QUAVER,45:Image.MUSIC_QUAVERS,46:Image.PITCHFORK,47:Image.XMAS,48:Image.PACMAN,49:Image.TARGET,50:Image.TSHIRT,51:Image.ROLLERSKATE,52:Image.DUCK,53:Image.HOUSE,54:Image.TORTOISE,55:Image.BUTTERFLY,56:Image.STICKFIGURE,57:Image.GHOST,58:Image.SWORD,59:Image.GIRAFFE,60:Image.SKULL,61:Image.UMBRELLA,62:Image.SNAKE,63:Image.HEART_SMALL}
def map(a,x1,y1,x2,y2):return int((a-x1)*(y2-x2)/(y1-x1)+x2)
def hi_nib(pb):return p[pb]>>4&15
def lo_nib(pb):return p[pb]&15
def get_nib(pb,nib):
	if nib:return p[pb]&15
	else:return p[pb]>>4&15
def set_nib(pb,nib,v):
	if nib:p[pb]=p[pb]&240|v
	else:p[pb]=v<<4|p[pb]&15
def save(fn):
	try:os.remove(fn)
	except OSError:writeln(RWE%fn)
	with open(fn,'wb')as mb:mb.write(p)
def load(fn):
	try:
		with open(fn,'rb')as mb:mb.readinto(p)
	except OSError:writeln(RWE%fn)
def hexToByte(c):
	if c>='0'and c<='9':return ord(c)-ord('0')
	if c>='A'and c<='F':return ord(c)-ord('A')+10
def nibbleToHex(value):
	c=value&15
	if c>=0 and c<=9:return c+ord('0')
	if c>=10 and c<=15:return c+ord('A')-10
def writeln(msg):uart.write(msg);uart.write(CR)
def printCheckSum(value):checksum=value&255;checksum=(checksum^255)+1;printHex8(checksum);uart.write(CR)
def printHex4(num):tmp=bytearray(1);tmp[0]=nibbleToHex(num);uart.write(tmp)
def printHex8(num):tmp=bytearray(2);tmp[0]=nibbleToHex(num>>4);tmp[1]=nibbleToHex(num);uart.write(tmp)
def printHex16(num):printHex8(num>>8);printHex8(num)
def wh():writeln('waiting for command:');writeln('w: write HEX file, r: read file, e: end')
def getNextChar():
	while not uart.any():sleep(10)
	c=uart.read(1);return chr(c[0])
def getMidiNote(note):
	if note>=32 and note<=108:tune=music_note[note%12]+chr(ord('2')+int(note/12))+':32';return tune
	return'C0:1'
def tansAcc(value):return map(value,-2000,2000,0,256)
def rci(p):
    t=int(machine.time_pulse_us(p,1,40000))
    if t<1000: return 0
    if t>2000: return 255
    return map(t,1000,2000,0,256)
def do(i,v):display.set_pixel(4-i,0,9*v);DO[i].write_digital(v)
def sp(v):
	for i in range(4):do(i,bool(v&1<<i))
def si():
	t=0
	for i in range(4):t=t+(DI[i].read_digital()<<i)
	sh(t,1);return t
def writeProgramSerial():
	display.show(Image.ARROW_N);writeln('program data:');checksum=0
	for pc in range(E2E):
		value=p[pc]
		if pc%8==0:
			if pc>0:printCheckSum(checksum)
			checksum=0;uart.write(':08');checksum+=8;printHex16(pc);checksum+=pc>>8;checksum+=pc&255;uart.write('00')
		printHex8(value);checksum+=value
	printCheckSum(checksum);writeln(':00000001FF')
def serialprg(br):
	display.show(Image.DIAMOND);eOfp=BF;uart.init(baudrate=br);uart.write(CR);writeln(PN);wh()
	while not eOfp:
		while uart.any():
			c=uart.read(1);ch=chr(c[0])
			if ch=='w':
				display.show(Image.ARROW_S);writeln('ready');eOfF=BF;data=bytearray(32)
				while BT:
					for i in range(8):data[i]=255
					while BT:
						c=getNextChar()
						if c==':':break
					c=getNextChar();count=hexToByte(c)<<4;c=getNextChar();count+=hexToByte(c);crc=count;c=getNextChar();readAddress=hexToByte(c)<<12;c=getNextChar();readAddress+=hexToByte(c)<<8;c=getNextChar();readAddress+=hexToByte(c)<<4;c=getNextChar();readAddress+=hexToByte(c);crc+=readAddress>>8;crc+=readAddress&255;c=getNextChar();type=hexToByte(c)<<4;c=getNextChar();type+=hexToByte(c);crc+=type
					if type==1:eOfF=BT
					for x in range(count):c=getNextChar();value=hexToByte(c)<<4;c=getNextChar();value+=hexToByte(c);data[x]=value;crc+=value
					c=getNextChar();readcrc=hexToByte(c)<<4;c=getNextChar();readcrc+=hexToByte(c);crc+=readcrc;value=crc&255
					if value==0:
						uart.write('ok')
						for x in range(count):p[readAddress+x]=data[x]
					else:writeln(', CRC Error');eOfF=BT
					writeln('')
					if eOfF:break
				writeln('endOfFile');save(TFN)
			elif ch=='r':load(TFN);writeProgramSerial()
			elif ch=='e':writeln('end');eOfp=BT
			else:wh()
	display.clear()
def sh(v,r):
	for i in range(4):display.set_pixel(4-i,r,9*(v>>i&1))
def wp():
	while PRG.is_pressed():0
def prg():
	load(TFN);display.show(Image.TSHIRT);wp();display.clear();PC=0;PM=BT
	while PM:
		IN=p[PC]>>4;DT=p[PC]&15;sh(IN,0);sh(DT,1);sh(PC,4);sh(PC>>4,3);display.set_pixel(0,0,5);display.set_pixel(0,1,0);ED=BT;NE=BT
		while ED:
			while not(PRG.is_pressed()or SEL.is_pressed()):0
			sleep(100)
			if PRG.is_pressed()and SEL.is_pressed():PM=BF;break
			if SEL.is_pressed():
				if NE:NE=BF;IN=-1
				while SEL.is_pressed():IN=IN+1&15;p[PC]=(IN<<4)+DT;sh(IN,0);sleep(250)
				continue
			ED=BF
		if not PM:break
		display.set_pixel(0,0,0);display.set_pixel(0,1,5);wp();ED=BT;NE=BT
		while ED:
			while not(PRG.is_pressed()or SEL.is_pressed()):0
			sleep(100)
			if PRG.is_pressed()and SEL.is_pressed():PM=BF;break
			if SEL.is_pressed():
				if NE:NE=BF;DT=-1
				while SEL.is_pressed():DT=DT+1&15;p[PC]=(IN<<4)+DT;sh(DT,1);sleep(250)
				continue
			ED=BF
		wp();sleep(100);PC=PC+1
		if PC>=E2E:break
	display.show(Image.YES);save(TFN);sleep(1000)
def init():
	for i in range(E2E):p[i]=255
	for i in range(4):DI[i].set_pull(DI[i].PULL_UP)
	for i in range(6):SB[i]=0
def dgo(d):
	if d:writeln('dbg on')
	else:writeln('dbg off')
def run():
	DBG=pin_logo.is_touched();dgo(DBG);uart.init(baudrate=BR);uart.write(CR);writeln(PN+'\r\nrunning microbit TPS\r\nd: toggle debug, p:program mode');A=0;B=0;C=0;D=0;E=0;F=0;PC=0;PG=0;RT=0;IN=0;DT=0;STP=0;load(TFN);display.clear()
	for i in range(E2E):
		IN=hi_nib(i)
		if IN==14:
			DT=lo_nib(i)
			if DT>=8 and DT<=13:SB[DT-8]=i
	while BT:
		IN=p[PC]>>4;DT=p[PC]&15
		if uart.any():
		    c=uart.read(1);ch=chr(c[0])
		    if ch=='d':DBG=not DBG;dgo(DBG);
		    if ch=='p':serialprg(BR);reset();
		if DBG:
			writeln('-');uart.write('PC: ');printHex16(PC);writeln('');uart.write('INST: ');printHex4(IN);uart.write(', DATA: ');printHex4(DT);writeln('');writeln('Register:');uart.write('A: ');printHex8(A);uart.write(', B: ');printHex8(B);uart.write(', C: ');printHex8(C);writeln('');uart.write('D: ');printHex8(D);uart.write(', E: ');printHex8(E);uart.write(', F: ');printHex8(F);writeln('');uart.write('Page: ');printHex8(PG);uart.write(', Ret: ');printHex16(RT);writeln('')
			if ST:
				line=''
				while not line:line=uart.readline()
		if IN==0:
			if DT==1:display.set_pixel(A,B,9)
			if DT==2:display.set_pixel(A,B,0)
			if DT==3:
				if A==0:display.clear()
				else:image=images.get(A,Image.SAD);display.show(image)
		if IN==1:sp(DT)
		if IN==2:
			if DT==14:slp=30000
			if DT==15:slp=60000
			else:slp=10**(DT//3)*WT[DT%3]
			sleep(slp)
		if IN==3:PC=PC-DT-1
		if IN==4:A=DT
		if IN==5:
			if DT==0:tmp=A;A=B;B=tmp
			if DT==1:B=A
			if DT==2:C=A
			if DT==3:D=A
			if DT==4:sp(A)
			if DT>4 and DT<=8:do(DT-5,A&1)
			if DT>8 and DT<=10:AO[DT-9].set_analog_period(2);AO[DT-9].write_analog((A&15)*64)
			if DT>10 and DT<=12:AO[DT-11].set_analog_period(20);AO[DT-9].write_analog((A&15)*64)
			if DT==13:E=A
			if DT==14:F=A
			if DT==15:
				STK[STP]=A;STP+=1
				if STP>15:STP=15
		if IN==6:
			if DT==1:A=B
			if DT==2:A=C
			if DT==3:A=D
			if DT==4:A=si()
			if DT>4 and DT<=8:A=DI[DT-5].read_digital()
			if DT>8 and DT<=10:display.off();A=AI[DT-9].read_analog()//64;display.on()
			if DT==11:display.off();A=rci(AI[0])>>4;display.on()
			if DT==12:display.off();A=rci(AI[1])>>4;display.on()
			if DT==13:A=E
			if DT==14:A=F
			if DT==15:
				STP-=1
				if STP<0:STP=0
				A=STK[STP]
		if IN==7:
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
		if IN==8:PG=DT*16
		if IN==9:PC=PG+DT;continue
		if IN==10:
			if C>0:C=C-1;PC=PG+DT;continue
		if IN==11:
			if D>0:D=D-1;PC=PG+DT;continue
		if IN==12:
			s=BF
			if DT==0:s=A==0
			if DT==1:s=A>B
			if DT==2:s=A<B
			if DT==3:s=A==B
			if DT>=4 and DT<=7:s=DI[DT%4].read_digital()&1==1
			if DT>=8 and DT<=11:s=DI[DT%4].read_digital()&1==0
			if DT==12:s=PRG.is_pressed()
			if DT==13:s=SEL.is_pressed()
			if DT==14:s=not PRG.is_pressed()
			if DT==15:s=not SEL.is_pressed()
			if s:PC=PC+1
		if IN==13:RT=PC+1;PC=PG+DT;continue
		if IN==14:
			if DT==0:PC=RT-1
			if DT>=1 and DT<=6:RT=PC;PC=SB[DT-1];continue
			if DT==15:reset()
		if IN==15:
			if DT==0:display.off();A=int(AI[0].read_analog()>>2);display.on()
			if DT==1:display.off();A=int(AI[1].read_analog()>>2);display.on()
			if DT==2:display.off();A=rci(AI[0]);display.on()
			if DT==3:display.off();A=rci(AI[1]);display.on()
			if DT==4:AO[0].set_analog_period(2);AO[0].write_analog(A<<4)
			if DT==5:AO[1].set_analog_period(2);AO[1].write_analog(A<<4)
			if DT==6:AO[0].set_analog_period(20);AO[0].write_analog(int(A/2))
			if DT==7:AO[1].set_analog_period(20);AO[1].write_analog(int(A/2))
			if DT==8:
				if A==0:music.pitch(0,duration=1,wait=BF)
				if A>0:f=440*2**((A-69)/12);music.pitch(int(f),duration=-1,wait=BF)
			if DT==9:A=tansAcc(accelerometer.get_x());E=tansAcc(accelerometer.get_y());F=tansAcc(accelerometer.get_z())
			if DT==10:
				if not compass.is_calibrated:compass.calibrate()
				A=int(compass.heading()/5)
			if DT==11:mic_val=int(microphone.sound_level()/255*16);A=mic_val
			if DT==12:A=display.read_light_level()
			if DT==13:A=pin_logo.is_touched()
			if DT==14:
				g=accelerometer.current_gesture();A=0
				if g=='up':A=1
				if g=='down':A=2
				if g=='left':A=3
				if g=='right':A=4
				if g=='face up':A=5
				if g=='face down':A=6
				if g=='freefall':A=7
				if g=='3g':A=8
				if g=='6g':A=9
				if g=='8g':A=10
				if g=='shake':A=11
			if DT==15:PC=0;continue
		A=A&255;B=B&255;C=C&255;D=D&255;E=E&255;F=F&255;PC=(PC+1)%E2E
init()
if PRG.is_pressed():prg()
if SEL.is_pressed():serialprg(9600)
run()