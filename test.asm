.arduinotps ; switch to arduinotps

:loop1
LDA ADC1
MOV B,A
LDA ADC2
BYTE
BSTA SRV1
RJMP :loop1
