

class CommandSet:
    DELAYTIMES = [1 , 2 , 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 30000, 60000]

    commands = {0x00: "NOP", 0x10: "Output", 0x20: "Delay", 0x30: "Jump Back", 0x40: "A=", 0x50: "*=A", 0x60: "A=*", 0x70: "CALC",
                0x80: "PAGE", 0x90: "Jump", 0xA0: "Jump if C", 0xB0: "Jump if D", 0xC0: "Skip", 0xD0: "Call", 0xE0: "Ret/Callsub", 0xF0: "Byte"}

    def GetCommentsForCommand(self, command):
        if command < 0x10:
            return self.commands[0x00]
        elif 0x10 <= command < 0x20:
            return self.commands[0x10] + " {:04b}".format(command & 0x0F)
        elif command < 0x30:
            return self.commands[0x20] + " {:d}ms".format(self.DELAYTIMES[command & 0x0F])
        elif command < 0x40:
            return self.commands[0x30] + " -{:d}".format(command & 0x0F)
        elif command < 0x50:
            return self.commands[0x40] + "{:d}".format(command & 0x0F)
        elif command < 0x60:
            return self.commands[0x50]
        elif command < 0x70:
            return self.commands[0x60]
        elif command < 0x80:
            return self.commands[0x70]
        elif command < 0x90:
            return self.commands[0x80] + " {:d}".format(command & 0x0F)
        elif command < 0xA0:
            return self.commands[0x90] + " Page * 16 + {:d}".format(command & 0x0F)
        elif command < 0xB0:
            return self.commands[0xA0] + " {:d}".format(command & 0x0F)
        elif command < 0xC0:
            return self.commands[0xB0] + " {:d}".format(command & 0x0F)
        elif command < 0xD0:
            return self.commands[0xC0] + " {:d}".format(command & 0x0F)
        elif command < 0xE0:
            return self.commands[0xD0] + " Page * 16 + {:d}".format(command & 0x0F)
        elif command < 0xF0:
            return self.commands[0xE0]
        elif command <= 0xFF:
            return self.commands[0xF0]
        else:
            return "NOP"
