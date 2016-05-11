#!/bin/bash

mkdir tmp
cd tmp

#OpenCV
mkdir opencv
cd opencv
wget http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.11/opencv-2.4.11.zip
unzip opencv-2.4.11.zip
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j4
sudo make install
cd ../..
rm -rf opencv


#OpenBR
git clone https://github.com/biometrics/openbr.git
cd openbr
git checkout v1.1.0
git submodule init
git submodule update
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DBR_INSTALL_BRPY=ON ..
make -j4
sudo make install







