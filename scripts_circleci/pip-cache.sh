#!/bin/sh

if [ ! -e ~/pipcache ]; then
    mkdir ~/pipcache
fi

/opt/circleci/.pyenv/versions/2.7.11/bin/pip install --download-cache="/home/ubuntu/pipcache" -r requeriments.txt
