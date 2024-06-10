#!/bin/bash

sudo apt install xorg libxkbcommon-dev libxkbcommon-tools libxkbcommon-x11-0 \
    libfontconfig1

mamba install libxcb

echo 'export LD_LIBRARY_PATH=$CONDA_PREIX/lib:${LD_LIBRARY_PATH}' >> $HOME/.bashrc