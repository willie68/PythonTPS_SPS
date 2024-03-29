# Raspberry Pi Pico TPS

This is my implementation of the TPS on Raspberry Pi Pico. The instructions will be compatible to my ArduinoTPS Version. If you find a bug, feel free to create a issue in the tracker. 

# Installation

There are 2 possible way to install the pico tps to the Raspberry Pi Pico.

## Simple

First the simplest version. 

- get the pico-tps.uf2 file from a github release page (https://github.com/willie68/PythonTPS_SPS/releases)
- start the pico with botsel pressed
- copy the uf2 file to the created pico drive

After the automated restart, the tps is up running. 

## with MicroPython and Thonny

If you want to look behind the scenes of the pico python tps you can do the second install option.

At the moment the installation process is quite complicated. So you need to install Thonny IDE for that. (https://thonny.org/)

1. Start the Pico with BOTSEL pressed. A new drive on your PC will appear. 
2. Copy the firmware rp2-pico-###########.uf2 to this drive. Wait until restart.
3. Start your Thonny IDE, connect with the Pico. 
4. Upload the main.py to the Pico. Restart (without BOTSEL). Now TPS is up and running. 

If you brick your Pico, you cant connect with thonny to the Pico, start the Pico with BOTSEL pressed. A new drive on your PC will appear. Copy the firmware MicroPython_RenameMainDotPy.uf2 to this drive. Wait until restart. Than start at the beginning again.

# Command implementation Chart

The actual command implementation list: 

|      | 0         | 1           | 2            | 3                         | 4         | 5                | 6            | 7                     |
| ---- | --------- | ----------- | ------------ | ------------------------- | --------- | ---------------- | ------------ | --------------------- |
|      | n.n.      | Port [DOUT] | Delay [WAIT] | Jump back relative [RJMP] | A=# [LDA] | =A               | A=           | A=Ausdruck            |
| 0    | NOP [NOP] | aus         | 1ms          | 0                         | 0         | A<->B [SWAP]     |              |                       |
| 1    |           | 1           | 2ms          | 1                         | 1         | B=A [MOV]        | A=B [MOV]    | A=A + 1 [INC]         |
| 2    |           | 2           | 5ms          | 2                         | 2         | C=A [MOV]        | A=C [MOV]    | A=A - 1 [DEC]         |
| 3    |           | 3           | 10ms         | 3                         | 3         | D=A [MOV]        | A=D [MOV]    | A=A + B [ADD]         |
| 4    |           | 4           | 20ms         | 4                         | 4         | Dout=A [STA]     | Din [LDA]    | A=A - B [SUB]         |
| 5    |           | 5           | 50ms         | 5                         | 5         | Dout.1=A.1 [STA] | Din.1 [LDA]  | A=A * B [MUL]         |
| 6    |           | 6           | 100ms        | 6                         | 6         | Dout.2=A.1 [STA] | Din.2 [LDA]  | A=A / B [DIV]         |
| 7    |           | 7           | 200ms        | 7                         | 7         | Dout.3=A.1 [STA] | Din.3 [LDA]  | A=A and B [AND]       |
| 8    |           | 8           | 500ms        | 8                         | 8         | Dout.4=A.1 [STA] | Din.4 [LDA]  | A=A or B [OR]         |
| 9    |           | 9           | 1s           | 9                         | 9         | PWM.1=A [STA]    | ADC.1 [LDA]  | A=A xor B [XOR]       |
| a    |           | 10          | 2s           | 10                        | 10        | PWM.2=A [STA]    | ADC.2 [LDA]  | A= not A [NOT]        |
| b    |           | 11          | 5s           | 11                        | 11        | Servo.1=A [STA]  | RCin.1 [LDA] | A= A % B (Rest) [MOD] |
| c    |           | 12          | 10s          | 12                        | 12        | Servo.2=A [STA]  | RCin.2 [LDA] | A= A + 16 * B [BYTE]  |
| d    |           | 13          | 20s          | 13                        | 13        | E=A [MOV]        | A=E [MOV]    | A= B - A[BSUBA]       |
| e    |           | 14          | 30s          | 14                        | 14        | F=A [MOV]        | A=F [MOV]    | A=A SHR 1 [SHR]       |
| f    |           | 15          | 60s          | 15                        | 15        | Push A [PUSH]    | Pop A [POP]  | A=A SHL 1 [SHL]       |



|      | 8           | 9                              | a                                                     | b                                                    | c                 | d                         | e              | f                |
| ---- | ----------- | ------------------------------ | ----------------------------------------------------- | ---------------------------------------------------- | ----------------- | ------------------------- | -------------- | ---------------- |
|      | Page [PAGE] | Jump absolut (#+16*page) [JMP] | C* C>0: C=C-1;             Jump # + (16*page) [LOOPC] | D* D>0:D=D-1;             Jump # + (16*page) [LOOPC] | Skip if           | Call # + (16*Page) [Call] | Callsub/Ret    | Byte Befehle     |
| 0    | 0           | 0                              | 0                                                     | 0                                                    | A==0 [SKIP0]      | 0                         | ret [RTR]      | A=ADC.1 [BLDA]   |
| 1    | 1           | 1                              | 1                                                     | 1                                                    | A>B [AGTB]        | 1                         | Call 1 [CASB]  | A=ADC.2 [BLDA]   |
| 2    | 2           | 2                              | 2                                                     | 2                                                    | A<B [ALTB]        | 2                         | 2 [CASB]       | A=RCin.1 [BLDA]  |
| 3    | 3           | 3                              | 3                                                     | 3                                                    | A==B [AEQB]       | 3                         | 3 [CASB]       | A=RCin.2 [BLDA]  |
| 4    | 4           | 4                              | 4                                                     | 4                                                    | Din.1==1 [DEQ1 1] | 4                         | 4 [CASB]       | PWM.1=A [BSTA]   |
| 5    | 5           | 5                              | 5                                                     | 5                                                    | Din.2==1 [DEQ1 2] | 5                         | 5 [CASB]       | PWM.2=A [BSTA]   |
| 6    | 6           | 6                              | 6                                                     | 6                                                    | Din.3==1 [DEQ1 3] | 6                         | 6 [CASB]       | Servo.1=A [BSTA] |
| 7    | 7           | 7                              | 7                                                     | 7                                                    | Din.4==1 [DEQ1 4] | 7                         |                | Servo.2=A [BSTA] |
| 8    | 8           | 8                              | 8                                                     | 8                                                    | Din.1==0 [DEQ0 1] | 8                         | Def 1 [DFSB]   | Tone=A [TONE]    |
| 9    | 9           | 9                              | 9                                                     | 9                                                    | Din.2==0 [DEQ0 2] | 9                         | 2 [DFSB]       | PWM.3=A [BSTA]   |
| a    | 10          | 10                             | 10                                                    | 10                                                   | Din.3==0 [DEQ0 3] | 10                        | 3 [DFSB]       | PWM.4=A [BSTA]   |
| b    | 11          | 11                             | 11                                                    | 11                                                   | Din.4==0 [DEQ0 4] | 11                        | 4 [DFSB]       | Servo.3=A [BSTA] |
| c    | 12          | 12                             | 12                                                    | 12                                                   | S_PRG==0 [PRG0]   | 12                        | 5 [DFSB]       | Servo.4=A [BSTA] |
| d    | 13          | 13                             | 13                                                    | 13                                                   | S_SEL==0 [SEL0]   | 13                        | 6 [DFSB]       | LED on [LED1]    |
| e    | 14          | 14                             | 14                                                    | 14                                                   | S_PRG==1 [PRG1]   | 14                        |                | LED off [LED0]   |
| f    | 15          | 15                             | 15                                                    | 15                                                   | S_SEL==1 [SEL1]   | 15                        | restart [REST] | PrgEnd [PEND]    |



## Hardware assignments:

**Caution**: Due to the dual assignment of pins (especially the two A / D converters) can cause effects on the circuit in both directions. Protective diodes may be required there.

## Raspberry Pi Pico pin mapping table



| pin number | pico function  | TPS function | pin  | pico function | TPS function    |
| ---------- | -------------- | ------------ | ---- | ------------- | --------------- |
| 1          | GP0            |              | 40   | VBUS          |                 |
| 2          | GP1            |              | 39   | VSYS          |                 |
| 3          | GND            |              | 38   | GND           |                 |
| 4          | GP2            | Dout.1       | 37   | 3V3_EN        |                 |
| 5          | GP3            | Dout.2       | 36   | 3V3           |                 |
| 6          | GP4            | Dout.3       | 35   | ADC_VREF      |                 |
| 7          | GP5            | Dout.4       | 34   | ADC2          |                 |
| 8          | GND            |              | 33   | GND           |                 |
| 9          | GP6            | Din.1        | 32   | ADC1          | ADC.1           |
| 10         | GP7            | Din.2        | 31   | ADC0          | ADC.0           |
| 11         | GP8            | Din.3        | 30   | RUN           | Reset           |
| 12         | GP9            | Din.4        | 29   | GP22          |                 |
| 13         | GND            |              | 28   | GND           |                 |
| 14         | GP10           | SEL          | 27   | GP21          | PWM.4 (Servo.4) |
| 15         | GP11           | PRG          | 26   | GP20          | PWM.3 (Servo.3) |
| 16         | GP12, UART0 TX |              | 25   | GP19          |                 |
| 17         | GP13, UART0 RX |              | 24   | GP18          | Tone output     |
| 18         | GND            |              | 23   | GND           |                 |
| 19         | GP14           | RC.1         | 22   | GP17          | PWM.2 (Servo.2) |
| 20         | GP15           | RC.2         | 21   | GP16          | PWM.1 (Servo.1) |

# Apendix
