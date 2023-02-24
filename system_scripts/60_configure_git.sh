#!/bin/bash -exu

sudo apt install git

# git config

git config --global user.email "amazon-manipulation@cs.washington.edu"
git config --global user.name "UW Amazon Manipulation Project"

ssh-keyscan github.com | tee -a $HOME/.ssh/known_hosts 
ssh-keyscan gitlab.com | tee -a $HOME/.ssh/known_hosts 

ssh-keyscan 10.158.54.167 | tee -a $HOME/.ssh/known_hosts 
ssh-keyscan 10.158.54.168 | tee -a $HOME/.ssh/known_hosts 
