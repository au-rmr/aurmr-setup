#!/bin/bash -exu

sudo apt install cmake-curses-gui build-essential
sudo apt install --no-install-recommends kolourpaint feh kde-spectacle chromium-browser


# configure python
sudo apt install python3-pip 
pip install -U pip
pip install -U poetry


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


# git config


sudo apt install git
git config --global user.email "amazon-manipulation@cs.washington.edu"
git config --global user.name "UW Amazon Manipulation Project"


# setup fzf

cat >> $HOME/.bashrc <<EOF
if [ -f /usr/share/doc/fzf/examples/completion.bash ]; then
	source /usr/share/doc/fzf/examples/completion.bash

fi
if [ -f /usr/share/doc/fzf/examples/key-bindings.bash ]; then
	source /usr/share/doc/fzf/examples/key-bindings.bash
fi

export PATH=$PATH:$HOME/.local/bin
EOF
