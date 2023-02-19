#!/bin/bash

echo "Disabling unattended upgrades"

sudo dpkg-reconfigure unattended-upgrades

cat | sudo tee -a /etc/apt/apt.conf.d/01norecommend << EOF
APT::Install-Recommends "0";
APT::Install-Suggests "0";
EOF


# hostname
echo """Set the hostname with
sudo hostnamectl set-hostname 
<aurmr-perception/aurmr-control>"""
