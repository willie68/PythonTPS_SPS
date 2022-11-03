##### BUILDER #####

FROM tps-pico-prebuild as builder

## Task: Update ca certificates
RUN update-ca-certificates

## Task: get source files
RUN mkdir -p /home/pico-tps
WORKDIR /home/pico-tps

COPY  ./builder/build_tps.sh ./

RUN ./build_tps.sh