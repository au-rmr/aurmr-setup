#!/bin/bash -exu

sudo apt install cmake-curses-gui build-essential
sudo apt install --no-install-recommends kolourpaint feh kde-spectacle chromium-browser


# configure python
sudo apt install python3-pip 
pip install -U pip
pip install -U poetry


# install conda

sudo apt install curl 


mkdir temp
cd temp
curl -L -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh 
./Miniconda3-latest-Linux-x86_64.sh

conda config --set auto_activate_base false
conda install mamba -c conda-forge


# git config


sudo apt install git
git config --global user.email "amazon-manipulation@cs.washington.edu"
git config --global user.name "UW Amazon Manipulation Project"
