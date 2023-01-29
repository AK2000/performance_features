#!/bin/bash

apt update
apt install g++ gcc swig libpfm4-dev python3-dev python3-pip
cd profiler/
python3 setup.py build
python3 setup.py install
cd ..
pip3 install -r requirements.txt