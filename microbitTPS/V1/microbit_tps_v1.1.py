from microbit import *
import gc
gc.collect()
BT=True
BF=False
TFN='tps.bin'
E2E=256
p=bytearray(E2E)
SEL=button_a
PRG=button_b
DI1=pin13
DI2=pin14
DI3=pin15
DI4=pin16
DI=[DI1,DI2,DI3,DI4]
DO1=pin0
DO2=pin1
DO3=pin2
DO4=pin12
DO=[DO1,DO2,DO3,DO4]
AO1=pin8
AO2=pin9
AO=[AO1,AO2]
AI1=pin3
AI2=pin4
AI=[AI1,AI2]
def load():
	for i in range(E2E):p[i]=255
	with open(TFN,'rb')as mb:mb.readinto(p)
def save():
	with open(TFN,'wb')as mb:mb.write(p)
def nibbleToHex(value):
	c=value&15
	if c>=0 and c<=9:return c+ord('0')
	if c>9 and c<=15:return c+ord('A')-10
def do(i,v):display.set_pixel(4-i,0,9*v);DO[i].write_digital(v)
def sp(v):
	for i in range(4):do(i,bool(v&1<<i))
def si():
	t=0
	for i in range(4):t=t+DI[i].read_digital()<<i
	return t
def sh(v,r):
	for i in range(4):display.set_pixel(4-i,r,9*(v>>i&1))
def wp():
	while PRG.is_pressed():0
def prg():
	display.show(Image.HEART);wp();display.clear();PC=0;PM=BT
	while PM:
		IN=p[PC]>>4;DT=p[PC]&15;sh(IN,0);sh(DT,1);sh(PC,4);sh(PC>>4,3);display.set_pixel(0,0,5);display.set_pixel(0,1,0);ED=BT
		while ED:
			while not(PRG.is_pressed()or SEL.is_pressed()):0
			sleep(100)
			if PRG.is_pressed()and SEL.is_pressed():PM=BF;break
			if SEL.is_pressed():
				while SEL.is_pressed():IN=IN+1&15;p[PC]=(IN<<4)+DT;sh(IN,0);sleep(250)
				continue
			ED=BF
		if not PM:break
		display.set_pixel(0,0,0);display.set_pixel(0,1,5);wp();ED=BT
		while ED:
			while not(PRG.is_pressed()or SEL.is_pressed()):0
			sleep(100)
			if PRG.is_pressed()and SEL.is_pressed():PM=BF;break
			if SEL.is_pressed():
				while SEL.is_pressed():DT=DT+1&15;p[PC]=(IN<<4)+DT;sh(DT,1);sleep(250)
				continue
			ED=BF
		wp();sleep(200);PC=PC+1
		if PC>=E2E:break
	save()
def run():
	WT=[1,2,5];DI1.set_pull(DI1.PULL_UP);DI2.set_pull(DI2.PULL_UP);DI3.set_pull(DI3.PULL_UP);DI4.set_pull(DI4.PULL_UP);PC=0;PG=0;RT=0;A=0;B=0;C=0;D=0;display.clear()
	while BT:
		IN=p[PC]>>4;DT=p[PC]&15
		if IN==1:sp(DT)
		if IN==2:
			if DT==14:sl=30000
			elif DT==15:sl=60000
			else:sl=10**(DT//3)*WT[DT%3]
			sleep(sl)
		if IN==3:PC=PC-DT-1
		if IN==4:A=DT
		if IN==5:
			if DT==0:t=A;A=B;B=t
			if DT==1:B=A
			if DT==2:C=A
			if DT==3:D=A
			if DT==4:sp(A)
			if DT>4 and DT<=8:do(DT-5,A&1)
			if DT>8 and DT<=9:AO[DT-9].write_analog(A&15*64)
		if IN==6:
			if DT==1:A=B
			if DT==2:A=C
			if DT==3:A=D
			if DT==4:A=si()
			if DT>4 and DT<=8:A=DI[DT-5].read_digital()
			if DT>8 and DT<=9:A=AI[DT-9].read_analog()//64
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
		if IN==8:PG=DT
		if IN==9:PC=PG*16+DT;continue
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
			if DT>3 and DT<=7:s=DI[DT-4].read_digital()
			if DT>7 and DT<=11:s=not DI[DT-8].read_digital()
			if DT==12:s=PRG.is_pressed()
			if DT==13:s=SEL.is_pressed()
			if DT==14:s=not PRG.is_pressed()
			if DT==15:s=not SEL.is_pressed()
			if s:PC=PC+1
		if IN==13:RT=PC+1;PC=PG+DT;continue
		if IN==14:
			if DT==0:PC=RT-1
		if IN==15:
			if DT==15:PC=0;continue
		A=A&16;PC=(PC+1)%E2E
load()
if PRG.is_pressed():prg()
run()