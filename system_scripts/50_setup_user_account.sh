#!/bin/bash -exu

sudo apt install cmake-curses-gui build-essential
sudo apt install --no-install-recommends kolourpaint feh kde-spectacle chromium-browser


# configure python
sudo apt install ipython3
sudo apt install python3-pip 
pip install -U pip
pip install -U poetry


# git config


sudo apt install git
git config --global user.email "amazon-manipulation@cs.washington.edu"
git config --global user.name "UW Amazon Manipulation Project"


# setup bash: configure fzf, PATH and user script
user_setup_script=$HOME/aurmr-setup/user_scripts/aurmr_setup.bashrc
#user_setup_script=$( dirname -- "$0"; )
#user_setup_script="${user_setup_script}/../user_scripts/setup.bash"
#user_setup_script=$( readlink -f "${user_setup_script}" )

cat >> $HOME/.bashrc <<EOF
if [ -f /usr/share/doc/fzf/examples/completion.bash ]; then
	source /usr/share/doc/fzf/examples/completion.bash

fi
if [ -f /usr/share/doc/fzf/examples/key-bindings.bash ]; then
	source /usr/share/doc/fzf/examples/key-bindings.bash
fi

source $user_setup_script

export PATH=\$PATH:$HOME/.local/bin
EOF

ssh-keyscan github.com | tee -a $HOME/.ssh/known_hosts 
ssh-keyscan gitlab.com | tee -a $HOME/.ssh/known_hosts 

ssh-keyscan 10.158.54.167 | tee -a $HOME/.ssh/known_hosts 
ssh-keyscan 10.158.54.168 | tee -a $HOME/.ssh/known_hosts 
