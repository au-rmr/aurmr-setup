#!/bin/bash -eux

sudo apt install fuse3 sshfs

sudo mkdir /workspaces/
sudo chown $USER /workspaces

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


cat | sudo tee -a /etc/fstab <<EOF
aurmr@${OTHER_HOST}:/home/aurmr/workspaces/  /workspaces/$OTHER_HOST/  fuse.sshfs x-systemd.automount,_netdev,user,exec,transform_symlinks,identityfile=/home/aurmr/.ssh/id_rsa,allow_other,default_permissions,uid=aurmr,gid=aurmr 0 0
EOF

