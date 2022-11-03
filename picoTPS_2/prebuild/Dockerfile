##### BUILDER #####

FROM ubuntu:22.04 as builder

## Task: Install build deps
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN set -eux; \
    apt-get install --no-install-recommends --allow-change-held-packages -y\
    git \
    wget \ 
    python3

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN apt-get install --no-install-recommends --allow-change-held-packages -y\
    gcc-arm-none-eabi \
    libstdc++-arm-none-eabi-newlib \
    libnewlib-arm-none-eabi
RUN apt-get install --no-install-recommends --allow-change-held-packages -y\
    build-essential \
    cmake
RUN apt-get install apt-transport-https ca-certificates -y
RUN apt install software-properties-common -y
RUN apt-get install gettext uncrustify -y
