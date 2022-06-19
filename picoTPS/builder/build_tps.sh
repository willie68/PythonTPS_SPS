git clone https://github.com/micropython/micropython.git
cd micropython
git submodule update --init lib/mbedtls

make -C mpy-cross

cd ./ports/rp2

copy ./main.py ./modules/main.py 

make submodules
make clean
make