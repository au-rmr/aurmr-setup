#!/bin/bash -exu


# install conda

sudo apt install curl 


TEMP_DIR=$(mktemp -d miniconda_XXXXXXXXXX)
cd $TEMP_DIR


curl -L -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh 
./Miniconda3-latest-Linux-x86_64.sh


eval "$($HOME/miniconda3/bin/conda shell.bash hook)"

conda init bash zsh

conda install mamba -c conda-forge

conda config --set auto_activate_base false

