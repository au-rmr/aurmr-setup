#!/bin/bash -eux

sudo apt install fuse3 sshfs

sudo mkdir /workspaces/
sudo chown $USER /workspaces

static_hostname=$(hostnamectl status --static)

if [[ $static_hostname == "emmons" ]]; then
	ln -s /home/aurmr/workspaces /workspaces/emmons
	mkdir /workspaces/winthrop
	mkdir /workspaces/inter

cat | sudo tee -a /etc/fstab <<EOF
aurmr@winthrop:/home/aurmr/workspaces/  /workspaces/winthrop/  fuse.sshfs x-systemd.automount,_netdev,user,exec,transform_symlinks,identityfile=/home/aurmr/.ssh/id_rsa,allow_other,default_permissions,uid=aurmr,gid=aurmr 0 0
aurmr@inter:/home/aurmr/workspaces/  /workspaces/inter/  fuse.sshfs x-systemd.automount,_netdev,user,exec,transform_symlinks,identityfile=/home/aurmr/.ssh/id_rsa,allow_other,default_permissions,uid=aurmr,gid=aurmr 0 0
EOF
fi
if [[ $static_hostname == "winthrop" ]]; then
	ln -s /home/aurmr/workspaces /workspaces/winthrop
	mkdir workspaces/emmons
	mkdir workspaces/inter
cat | sudo tee -a /etc/fstab <<EOF
aurmr@emmons:/home/aurmr/workspaces/  /workspaces/emmons/  fuse.sshfs x-systemd.automount,_netdev,user,exec,transform_symlinks,identityfile=/home/aurmr/.ssh/id_rsa,allow_other,default_permissions,uid=aurmr,gid=aurmr 0 0
aurmr@inter:/home/aurmr/workspaces/  /workspaces/inter/  fuse.sshfs x-systemd.automount,_netdev,user,exec,transform_symlinks,identityfile=/home/aurmr/.ssh/id_rsa,allow_other,default_permissions,uid=aurmr,gid=aurmr 0 0
EOF
fi
if [[ $static_hostname == "inter" ]]; then
	ln -s /home/aurmr/workspaces /workspaces/inter
	mkdir workspaces/winthrop
	mkdir workspaces/emmons
cat | sudo tee -a /etc/fstab <<EOF
aurmr@emmons:/home/aurmr/workspaces/  /workspaces/emmons/  fuse.sshfs x-systemd.automount,_netdev,user,exec,transform_symlinks,identityfile=/home/aurmr/.ssh/id_rsa,allow_other,default_permissions,uid=aurmr,gid=aurmr 0 0
aurmr@winthrop:/home/aurmr/workspaces/  /workspaces/winthrop/  fuse.sshfs x-systemd.automount,_netdev,user,exec,transform_symlinks,identityfile=/home/aurmr/.ssh/id_rsa,allow_other,default_permissions,uid=aurmr,gid=aurmr 0 0
EOF
fi





