#!/bin/bash -eux

sudo apt update
sudo apt upgrade
sudo apt purge whoopsie

# add essential tools
sudo apt install vim tmux fzf zsh htop curl git
sudo apt install net-tools
sudo apt install lm-sensors

# ssh  server
sudo apt install openssh-server

# configure vim
sudo apt install vim-addon-manager vim-airline vim-syntastic vim-python-jedi vim-fugitive vim-ctrlp vim-youcompleteme
vim-addon-manager install airline
vim-addon-manager install ctrlp
vim-addon-manager install fugitive
vim-addon-manager install python-jedi
vim-addon-manager install syntastic
vim-addon-manager install youcompleteme

# install nvidia drivers
sudo ubuntu-drivers autoinstall

# ceate ssh key

ssh-keygen



mkdir $HOME/workspaces



sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8



sudo apt install software-properties-common
sudo add-apt-repository universe
