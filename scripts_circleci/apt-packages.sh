#!/bin/sh


if [ ! -e ~/aptcache ]; then
    mkdir ~/aptcache
    sudo add-apt-repository --yes ppa:ubuntu-sdk-team/ppa
    sudo apt-get -o dir::cache::archives="/home/ubuntu/aptcache" update; 
fi
sudo apt-get -o dir::cache::archives="/home/ubuntu/aptcache" install -y build-essential cmake cmake-curses-gui qt5-default libqt5svg5-dev qtcreator git autoconf automake build-essential libass-dev libfreetype6-dev libgpac-dev libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libx11-dev libxext-dev libxfixes-dev pkg-config texi2html zlib1g-dev yasm python-pip python-dev libpng-dev libeigen3-dev libgtk2.0-dev
sudo aptitude build-dep -y libopencv-dev
