#!/bin/bash -exu


# install conda

sudo apt install curl 


TEMP_DIR=$(mktemp -d -p . user_account_XXXXXXXXXX)
cd $TEMP_DIR


curl -L -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh 
./Miniconda3-latest-Linux-x86_64.sh

# reload the bash
source $HOME/.bashrc

conda config --set auto_activate_base false
conda install mamba -c conda-forge

