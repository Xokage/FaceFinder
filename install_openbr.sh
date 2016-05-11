#!/bin/bash

mkdir tmp
cd tmp

#Yasm
git clone git://github.com/yasm/yasm.git
cd yasm
./configure
make
sudo make install
cd ..

#x264
mkdir ~/ffmpeg_sources
cd ~/ffmpeg_sources
wget http://download.videolan.org/pub/x264/snapshots/last_x264.tar.bz2
tar xjf last_x264.tar.bz2
cd x264-snapshot*
./configure --enable-shared --enable-pic
make
sudo make install
sudo ldconfig -v

#ffmpeg
cd ~/ffmpeg_sources
wget http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
tar xjf ffmpeg-snapshot.tar.bz2
cd ffmpeg
./configure --extra-libs="-ldl" --enable-gpl --enable-libass --enable-libfreetype --enable-libtheora --enable-libvorbis --enable-libx264 --enable-nonfree --enable-x11grab --enable-shared --enable-pic
make
sudo make install
sudo ldconfig -v

#OpenCV
mkdir ~/opencv_sources
cd ~/opencv_sources
wget http://kent.dl.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.9/opencv-2.4.9.zip
unzip -qq opencv-2.4.9.zip
cd opencv-2.4.9
mkdir release
cd release
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_NEW_PYTHON_SUPPORT=ON ..
make
sudo make install
sudo ldconfig -v


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







