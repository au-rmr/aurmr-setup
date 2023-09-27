#!/bin/bash -eux

cat | sudo tee -a /etc/hosts <<EOF
192.168.10.101 control aurmr-control winthrop aurmr-winthrop
192.168.10.102 perception aurmr-perception inter aurmr-inter 
192.168.10.103 rt aurmr-rt emmons aurmr-emmons
EOF


