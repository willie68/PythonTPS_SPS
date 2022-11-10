git clone https://github.com/adafruit/circuitpython.git
cd circuitpython

make fetch-submodules

git checkout main

pip3 install --upgrade -r requirements-dev.txt
pip3 install --upgrade -r requirements-doc.txt

pre-commit install

make -C mpy-cross

pwd

cd ports/raspberrypi

mkdir modules

cp ../../../boot.py modules/boot.py
cp ../../../cody.py modules/code.py

make -j BOARD=raspberry_pi_pico
