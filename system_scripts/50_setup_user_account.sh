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

ssh-keyscan github.com | tee -a $HOME/.ssh/known_hosts 
ssh-keyscan gitlab.com | tee -a $HOME/.ssh/known_hosts 

ssh-keyscan 10.158.54.167 | tee -a $HOME/.ssh/known_hosts 
ssh-keyscan 10.158.54.168 | tee -a $HOME/.ssh/known_hosts 
