#!/bin/bash
#x264
if [ ! -e ~/ffmpeg_sources ]; then
    mkdir ~/ffmpeg_sources
    cd ~/ffmpeg_sources
    wget http://download.videolan.org/pub/x264/snapshots/last_x264.tar.bz2
    tar xjf last_x264.tar.bz2
    cd x264-snapshot*
    ./configure --enable-shared --enable-pic
    make
    sudo make install
else
    cd ~/ffmpeg_sources/x264-snapshot*
    sudo make install
fi

#OpenCV
if [ ! -e ~/opencv_sources ]; then
    mkdir ~/opencv_sources
    cd ~/opencv_sources
    wget http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.11/opencv-2.4.11.zip
    unzip -qq opencv-2.4.11.zip
    cd opencv-2.4.11
    mkdir build
    cd build
    cmake -D CMAKE_BUILD_TYPE=RELEASE -D WITH_FFMPEG=OFF ..
    make -j4
    sudo make install
else
    cd ~/opencv_sources/opencv-2.4.11/build
    sudo make install
fi

#OpenBR
if [ ! -e ~/openbr ]; then
    cd
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
else
    cd ~/openbr/build
    sudo make install
fi




