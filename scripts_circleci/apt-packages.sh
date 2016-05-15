#!/bin/sh


if [ ! -e ~/aptcache ]; then
    mkdir ~/aptcache
    sudo add-apt-repository --yes ppa:ubuntu-sdk-team/ppa
    sudo apt-add-repository -y 'deb http://ppa.launchpad.net/ondrej/mysql-experimental/ubuntu precise main'
    sudo apt-get -o dir::cache::archives="/home/ubuntu/aptcache" update; 
    sudo DEBIAN_FRONTEND=noninteractive apt-get -o dir::cache::archives="/home/ubuntu/aptcache" install -y mysql-server-5.6
    sudo apt-get -o dir::cache::archives="/home/ubuntu/aptcache" install -y build-essential cmake cmake-curses-gui qt5-default libqt5svg5-dev qtcreator git autoconf automake build-essential libass-dev libfreetype6-dev libgpac-dev libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libx11-dev libxext-dev libxfixes-dev pkg-config texi2html zlib1g-dev yasm python-pip python-dev libpng-dev libeigen3-dev libgtk2.0-dev mysql-server-5.6
else
    sudo dpkg -i ~/aptcache/*.deb 
fi
sudo aptitude build-dep -y libopencv-dev
