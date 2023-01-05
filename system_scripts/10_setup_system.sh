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



# SSHFS

mkdir /home/aurmr/workspaces
sudo apt install fuse3 sshfs

sudo mkdir /workspaces/
sudo chown aurmr:aurmr /workspaces

static_hostname=$(hostnamectl status --static)

if [[ $static_hostname == "aurmr-perception" ]]; then
	OTHER_HOST=control
	THIS_HOST=perception
	ln -s /home/aurmr/workspaces /workspaces/perception
	mkdir /workspaces/control
fi
if [[ $static_hostname == "aurmr-control" ]]; then
	OTHER_HOST=perception
	THIS_HOST=control
	ln -s /home/aurmr/workspaces /workspaces/control
	mkdir workspaces/perception
fi

cat | sudo tee -a /etc/hosts <<EOF
192.168.10.101 control aurmr-control
192.168.10.102 perception aurmr-perception
EOF

cat | sudo tee -a /etc/fstab <<EOF
aurmr@${OTHER_HOST}:/home/aurmr/workspaces/  /workspaces/$OTHER_HOST/  fuse.sshfs x-systemd.automount,_netdev,user,exec,transform_symlinks,identityfile=/home/aurmr/.ssh/id_rsa,allow_other,default_permissions,uid=aurmr,gid=aurmr 0 0
EOF

