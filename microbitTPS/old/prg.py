def prg():
	PC=0;nib=0;moved=1;load(TFN)
	for i in range(2):
		for j in range(2):
			for k in range(4):
				if get_nib(i,j)&1<<k:display.set_pixel(4-k,i*2+j,7*bool(get_nib(i,j)&1<<k))
	for i in range(4):display.set_pixel(4-i,nib%4,9)
	while PRG.is_pressed():0
	while BT:
		if SEL.is_pressed()and PRG.is_pressed():
			save();display.clear()
			while SEL.is_pressed()and PRG.is_pressed():0
			break
		if SEL.is_pressed():
			if moved:moved=0;set_nib(PC,nib%2,15)
			set_nib(PC,nib%2,(get_nib(PC,nib%2)+1)%16);sleep(100)
		if PRG.is_pressed():
			moved=1;nib=(nib+1)%E2E;PC=nib>>1
			if nib%4==0:
				for i in range(2):
					for j in range(2):
						for k in range(4):display.set_pixel(4-k,i*2+j,7*bool(get_nib(PC+i,j)&1<<k))
			for i in range(4):display.set_pixel(0,i,5*bool(PC&1<<i))
			for i in range(4,8):display.set_pixel(4-(i-4),4,5*bool(PC&1<<i))
			for i in range(4):display.set_pixel(4-i,nib%4,9)
			sleep(100)
		for i in range(4):display.set_pixel(4-i,nib%4,7*bool(get_nib(PC,nib%2)&1<<i))
		sleep(100)