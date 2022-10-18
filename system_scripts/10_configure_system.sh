#!/bin/bash

echo "Disabling unattended upgrades"

sudo dpkg-reconfigure unattended-upgrades


# hostname
echo """Set the hostname with
sudo hostnamectl set-hostname 
<aurmr-perception/aurmr-control>"""
