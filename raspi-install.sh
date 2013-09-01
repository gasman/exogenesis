#!/bin/sh

sudo apt-get install python-dev libasound-dev
git clone https://github.com/superquadratic/rtmidi-python.git
cd rtmidi-python
python setup.py build
cd ..
cp rtmidi-python/build/lib.linux-armv6l-2.7/rtmidi_python.so .
