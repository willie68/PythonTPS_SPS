git clone https://github.com/adafruit/circuitpython.git
cd circuitpython

make fetch-submodules

git checkout main

apt install python3-pip -y

pip3 install --upgrade -r requirements-dev.txt
pip3 install --upgrade -r requirements-doc.txt

pre-commit install

make -C mpy-cross

cd ./ports/rasberrypi

copy ./main.py ./modules/main.py 

make BOARD=raspberry_pi_pico