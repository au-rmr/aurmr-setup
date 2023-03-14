#!/bin/bash -eux


# upgrade the system

sudo apt update
sudo apt upgrade

# disable unattended upgrades

sudo dpkg-reconfigure unattended-upgrades

# no install recommends

cat | sudo tee -a /etc/apt/apt.conf.d/01norecommend << EOF
APT::Install-Recommends "0";
APT::Install-Suggests "0";
EOF


# remove whoopsie 

sudo apt purge whoopsie

# add essential tools
sudo apt install vim tmux fzf zsh htop curl git
sudo apt install net-tools
sudo apt install lm-sensors

# ssh server
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

# for RT kernels IGNORE_PREEMPT_RT_PRESENCE=1  might help
# see https://gist.github.com/pantor/9786c41c03a97bca7a52aa0a72fa9387

# ceate ssh key

ssh-keygen

# create workspace

mkdir $HOME/workspaces



sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8



sudo apt install software-properties-common
sudo add-apt-repository universe
