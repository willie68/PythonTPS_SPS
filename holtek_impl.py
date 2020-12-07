from time import sleep
from collections import deque
from utils import constrain


class Input:
    def __init__(self):
        self.Din_0 = False
        self.Din_1 = False
        self.Din_2 = False
        self.Din_3 = False
        self.ADC_1 = 0
        self.ADC_2 = 0
        self.RC_1 = 0
        self.RC_2 = 0
        self.PRG = False
        self.SEL = False

    def Print(self):
        print("Input: {}{}{}{} ADC_1: {} ADC_2: {} RC_1: {} RC_2: {}".format(("X" if self.Din_3 else "0"), ("X" if self.Din_2 else "0"),
                                                                             ("X" if self.Din_1 else "0"), ("X" if self.Din_0 else "0"), self.ADC_1, self.ADC_2, self.RC_1, self.RC_2))
        print("SEL: {} PRG: {}".format(self.SEL, self.PRG))


class Output:
    def __init__(self):
        self.Reset()

    def Print(self):
        print("Output: {}{}{}{} PWM_1: {} PWM_2: {} Servo_1: {} Servo_2: {}".format(("X" if self.Dout_3 else "0"), ("X" if self.Dout_2 else "0"),
                                                                                    ("X" if self.Dout_1 else "0"), ("X" if self.Dout_0 else "0"), self.PWM_1, self.PWM_2, self.Servo_1, self.Servo_2))

    def Reset(self):
        self.Dout_0 = False
        self.Dout_1 = False
        self.Dout_2 = False
        self.Dout_3 = False
        self.PWM_1 = 0
        self.PWM_2 = 0
        self.Servo_1 = 0
        self.Servo_2 = 0


class Register:
    def __init__(self):
        self.Reset()

    def Print(self, SPSActive):
        if SPSActive:
            print("Page: {} Addr: {} A: {} B: {} C: {} D: {} E: {} F: {}".format(
                self.Page, self.Addr, self.A, self.B, self.C, self.D, self.E, self.F))
        else:
            print("Page: {} Addr: {} A: {} B: {} C: {} D: {}".format(
                self.Page, self.Addr, self.A, self.B, self.C, self.D))

    def Reset(self):
        self.Addr = 0
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.F = 0
        self.Page = 0
        self.Stack = deque()


class Holtek:
    DELAYTIMES = [1, 2, 5, 10, 20, 50, 100, 200, 500,
                  1000, 2000, 5000, 10000, 20000, 30000, 60000]

    def __init__(self, filename):
        self.filename = filename
        self.program = []
        self.Register = Register()
        self.Input = Input()
        self.Output = Output()
        self.cmd = 0
        self.Return = 0
        self.SPSActive = False

    def doReset(self):
        self.Register.Reset()
        self.Output.Reset()

    def getName(self):
        return self.filename

    def load(self, program):
        if type(program) == bytearray:
            self.program = program

    def Start(self):
        self.Register.Reset()

    def HasNext(self):
        return True if self.Register.Addr < len(self.program) else False

    def doPort(self, value):
        self.Output.Dout_0 = value & 0x01
        self.Output.Dout_1 = value & 0x02
        self.Output.Dout_2 = value & 0x04
        self.Output.Dout_3 = value & 0x08

    def doIsA(self, value):
        if value == 0:
            tmp = self.Register.A
            self.Register.A = self.Register.B
            self.Register.B = tmp
        elif value == 1:
            self.Register.B = self.Register.A
        elif value == 2:
            self.Register.C = self.Register.A
        elif value == 3:
            self.Register.D = self.Register.A
        elif value == 4:
            doPort(self.Register.A)
        elif value == 5:
            self.Output.Dout_0 = (self.Register.A & 0x01) > 0
        elif value == 6:
            self.Output.Dout_1 = (self.Register.A & 0x01) > 0
        elif value == 7:
            self.Output.Dout_2 = (self.Register.A & 0x01) > 0
        elif value == 8:
            self.Output.Dout_3 = (self.Register.A & 0x01) > 0
        elif value == 9:
            self.Output.PWM_1 = self.Register.A
        elif value == 10:
            self.Output.PWM_2 = self.Register.A
        elif value == 11:
            self.Output.Servo_1 = constrain(self.Register.A, 0, 255)
        elif value == 12:
            self.Output.Servo_2 = constrain(self.Register.A, 0, 255)
        elif value == 13:
            self.Register.E = self.Register.A
        elif value == 14:
            self.Register.F = self.Register.A
        elif value == 15:
            if self.Register.Stack.count < 17:
                self.Register.Stack.append(self.Register.A)

    def doAIs(self, value):
        if value == 1:
            self.Register.A = self.Register.B
        elif value == 2:
            self.Register.A = self.Register.C
        elif value == 3:
            self.Register.A = self.Register.D
        elif value == 4:
            self.Register.A = 1 if self.Input.Din_0 else 0 + 2 if self.Input.Din_1 else 0 + \
                4 if self.Input.Din_2 else 0 + 8 if self.Input.Din_3 else 0
        elif value == 5:
            self.Register.A = 1 if self.Input.Din_0 else 0
        elif value == 6:
            self.Register.A = 1 if self.Input.Din_1 else 0
        elif value == 7:
            self.Register.A = 1 if self.Input.Din_2 else 0
        elif value == 8:
            self.Register.A = 1 if self.Input.Din_3 else 0
        elif value == 9:
            self.Register.A = constrain(self.Input.ADC_1, 0, 15)
        elif value == 10:
            self.Register.A = constrain(self.Input.ADC_2, 0, 15)
        elif value == 11:
            self.Register.A = constrain(self.Input.RC_1, 0, 15)
        elif value == 12:
            self.Register.A = constrain(self.Input.RC_2, 0, 15)
        elif value == 13:
            self.Register.A = self.Register.E
        elif value == 14:
            self.Register.A = self.Register.F
        elif value == 15:
            if self.Register.Stack.count > 0:
                self.Register.A = self.Register.Stack.pop()

    def doCalc(self, value):
        if value == 1:
            self.Register.A += 1
        elif value == 2:
            self.Register.A -= 1
        elif value == 3:
            self.Register.A += self.Register.B
        elif value == 4:
            self.Register.A -= self.Register.B
        elif value == 5:
            self.Register.A *= self.Register.B
        elif value == 6:
            self.Register.A /= self.Register.B
        elif value == 7:
            self.Register.A &= self.Register.B
        elif value == 8:
            self.Register.A |= self.Register.B
        elif value == 9:
            self.Register.A ^= self.Register.A
        elif value == 10:
            self.Register.A = ~self.Register.A
        elif value == 11:
            self.Register.A %= self.Register.B
        elif value == 12:
            self.Register.A += self.Register.B * 16
        elif value == 13:
            self.Register.A = self.Register.B - self.Register.A
        elif value == 14:
            self.Register.A >>= 1
        elif value == 15:
            self.Register.A <<= 1

    def doSkip(self, value):
        if value == 0:
            return self.Register.A == 0
        elif value == 1:
            return self.Register.A > self.Register.B
        elif value == 2:
            return self.Register.A < self.Register.B
        elif value == 3:
            return self.Register.A == self.Register.B
        elif value == 4:
            return self.Input.Din_0
        elif value == 5:
            return self.Input.Din_1
        elif value == 6:
            return self.Input.Din_2
        elif value == 7:
            return self.Input.Din_3
        elif value == 8:
            return self.Input.Din_0 == false
        elif value == 9:
            return self.Input.Din_1 == false
        elif value == 10:
            return self.Input.Din_2 == false
        elif value == 11:
            return self.Input.Din_3 == false
        elif value == 12:
            return self.Input.PRG
        elif value == 13:
            return self.Input.SEL
        elif value == 14:
            return self.Input.PRG == false
        elif value == 15:
            return self.Input.SEL == false

    def doByte(self, value):
        if value == 0:
            self.Register.A = constrain(self.Input.ADC_1, 0, 255)
        elif value == 1:
            self.Register.A = constrain(self.Input.ADC_2, 0, 255)
        elif value == 2:
            self.Register.A = constrain(self.Input.RC_1, 0, 255)
        elif value == 3:
            self.Register.A = constrain(self.Input.RC_2, 0, 255)
        elif value == 4:
            self.Output.PWM_1 = constrain(self.Register.A, 0, 255)
        elif value == 5:
            self.Output.PWM_2 = constrain(self.Register.A, 0, 255)
        elif value == 6:
            self.Output.Servo_1 = constrain(self.Register.A, 0, 255)
        elif value == 7:
            self.Output.Servo_2 = constrain(self.Register.A, 0, 255)

    def Execute(self):
        addr = self.Register.Addr
        if addr >= len(self.program):
            self.Register.Addr = 0
            addr = 0

        self.cmd = self.program[addr]
        value = self.cmd & 0x0F
        addrInc = True
        Skip = False
        if self.cmd == 0x00:
            self.doReset()
            addrInc = False
            pass
        elif 0x10 <= self.cmd < 0x20:
            self.doPort(value)
        elif 0x20 <= self.cmd < 0x30:
            sleep(self.DELAYTIMES[value] / 1000)
        elif 0x30 <= self.cmd < 0x40:
            self.Register.Addr -= (value + 1)
        elif 0x40 <= self.cmd < 0x50:
            self.Register.A = value
        elif 0x50 <= self.cmd < 0x60:
            doIsA(value)
        elif 0x60 <= self.cmd < 0x70:
            doAIs(value)
        elif 0x70 <= self.cmd < 0x80:
            doCalc(value)
        elif 0x80 <= self.cmd < 0x90:
            self.Register.Page = value
        elif 0x90 <= self.cmd < 0xA0:
            self.Register.Addr = value + self.Register.Page * 8
            addrInc = False
        elif 0xA0 <= self.cmd < 0xB0:
            if self.Register.C > 0:
                self.Register.C -= 1
                self.Register.Addr = value + self.Register.Page * 8
                addrInc = False
        elif 0xB0 <= self.cmd < 0xC0:
            if self.Register.D > 0:
                self.Register.D -= 1
                self.Register.Addr = value + self.Register.Page * 8
                addrInc = False
        elif 0xC0 <= self.cmd < 0xD0:
            Skip = doSkip(value)
        elif 0xD0 <= self.cmd < 0xE0:
            Return = self.Register.Addr + 1
            self.Register.Addr = value + self.Register.Page * 8
            addrInc = False
        elif 0xE0 <= self.cmd < 0xF0:
            if self.cmd == 0xe0:
                self.Register.Addr = Return
                addrInc = False
            elif self.cmd == 0xef:
                self.doReset()
                addrInc = False
        elif 0xF0 <= self.cmd <= 0xFF:
            if self.cmd == 0xe0:
                pass
            elif self.cmd == 0xff:
                self.doReset()
                addrInc = False

        if Skip:
            self.Register.Addr += 1
        if addrInc:
            self.Register.Addr += 1
        return True if self.Register.Addr < 10 else False
