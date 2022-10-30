@echo off
".\3rd party\GoVersionSetter.exe" -i
md dest
echo pre build image

docker build  ./prebuild/ -t tps-pico-prebuild

echo build image with build-tps.sh
docker build  --no-cache ./ -t pico-tps-builder

echo run tps builder script
docker run --name pico-tps-builder pico-tps-builder bash
docker cp pico-tps-builder:/home/pico-tps/micropython/ports/rp2/build-PICO/firmware.uf2 ./dest/pico_tps.uf2
docker stop pico-tps-builder
@echo off
echo if you like to look into the container than please break this script at this point. (CTRL-C)
echo after that simply start the container again with "docker run -it --name arduino-tps-builder arduino-tps-builder bash"
echo you will find the builded artefacts on this computer in ../dest and on the docker container in ../dest
pause

docker rm pico-tps-builder