#!/bin/bash -eux

sudo apt update
sudo apt upgrade
sudo apt purge whoopsie

# add essential tools
sudo apt install vim tmux fzf zsh htop curl git
sudo apt install net-tools

# ssh  server
sudo apt install openssh-server

# configure vim
sudo apt install vim-addon-manager vim-airline vim-syntastic vim-python-jedi vim-fugitive vim-ctrlp
vim-addon-manager install airline
vim-addon-manager install ctrlp
vim-addon-manager install fugitive
vim-addon-manager install python-jedi
vim-addon-manager install syntastic

# install nvidia drivers
sudo ubuntu-drivers autoinstall


# ceate ssh key

ssh-keygen


