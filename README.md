# PythonTPS_SPS
A TPS/SPS interpreter/emulator written in python

# Installation

1. Download the files as zip from github. (Or doing a clone with git)
2. Copy all file into a folder
3. Install all requirements with:
   `pip install -r requirements.txt`
4. Start emulator with the single step execution with:
   `python tpsemu.py Blink.tps`

# tpsemu.py

This is a single step emulator. You can use TPS files as well as HEX files in IntelHex format. 

TPS Files as HEX Files can be created with the windows TPS/SPS Emulator: https://wkla.no-ip.biz/ArduinoWiki/doku.php?id=arduino:arduinosps:spsemu

You can find more information and the Instruction here: https://wkla.no-ip.biz/ArduinoWiki/doku.php?id=arduino:arduinosps



# tpsasm.py

You can program the tps with an assembler like file. Read here for more information about that:

https://wkla.no-ip.biz/ArduinoWiki/doku.php?id=arduino:arduinosps:tpsass



With 

```
python tpsasm.py <input file> [output filename]
```

you can assemble the file to intelhex format which can directly used with the tps and the tps emulator. This assembler call need an internet connection, because the assembler itself is cloud based and can be used from [here](http://wk-music.de/tps/assembler) , too.