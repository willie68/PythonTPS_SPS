# How to 

compile a new micropython image with a py file as autostart. 

(Windows Version)

First install, if not already done, docker desktop

Than start a ubuntu image with an interactive shell

`docker run -it -v c:\temp\ubuntu:/var/host ubuntu /bin/bash`

In this shell we have to install some packages for the build process

```
apt-get install git
apt-get install gcc-arm-none-eabi libstdc++-arm-none-eabi-newlib libnewlib-arm-none-eabi
apt-get install build-essential
apt-get install cmake
apt-get install python3
```

Now we can clone the micropython repo

```
git clone https://github.com/micropython/micropython.git

git submodule update --init lib/mbedtls
```

Now we have to build mpy-cross first

```
cd micropython
make -C mpy-cross
cd ..
```

After that we can copy from the host maschine our *.py file to ports/rp2/modules.

Our last step is to build the firmware

```
cd ports/rp2
make submodules
make clean
make

```

After that you can copy from build-PICO the firmware.uf2 file to the desired firmware file.
