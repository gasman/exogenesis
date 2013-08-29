#!/bin/bash

apt-get update
apt-get install -y xinit
apt-get install -y build-essential python python-dev python-setuptools python-pip
apt-get install -y alsa-utils libasound-dev
apt-get install -y mercurial libsdl-dev libsdl-mixer1.2-dev
adduser vagrant audio

sudo pip install virtualenvwrapper
# add:
# source /usr/local/bin/virtualenvwrapper.sh
# to ~/.bashrc
