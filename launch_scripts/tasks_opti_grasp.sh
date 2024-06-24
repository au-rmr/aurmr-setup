#!/bin/bash -e


echo "Please make sure that roscore is launched using launch_aurmr_core.sh"

echo "starting robot ..."
ssh emmons tmux new-session -d -s aurmr-emmons
ssh emmons tmux send-keys -t aurmr-emmons:0 "activate\ aurmr_demo"  C-m
ssh emmons tmux send-keys -t aurmr-emmons:0 "roslaunch\ tahoma_bringup\ tahoma_bringup.launch\ gui:=False" C-m
sleep 1
echo -n "done"
echo ""

echo "starting perception ..."
tmux new-session -d -s aurmr-inter
ssh inter tmux send-keys -t aurmr-inter:0 "activate\ aurmr_demo_opti_grasp"  C-m
ssh inter tmux send-keys -t aurmr-inter:0 "roslaunch\ aurmr_perception\ aurmr_perception_clustering.launch\ grasp_type:=RGB_grasp" C-m
sleep 1
echo -n "done"
echo ""

echo "starting statemachine ..."
ssh emmons tmux new-window -t aurmr-emmons
ssh emmons tmux send-keys -t aurmr-emmons:1 "activate\ aurmr_demo"  C-m
ssh emmons tmux send-keys -t aurmr-emmons:1 "cd\ /home/aurmr/workspaces/aurmr_demo/src/aurmr_tahoma/aurmr_tasks/scripts" C-m
ssh emmons tmux send-keys -t aurmr-emmons:1 "python\ aurmr_demo"
sleep 3
ssh emmons tmux send-keys -t aurmr-emmons:1 "C-m"
echo -n "done"
echo ""


echo "starting stowing script ..."
ssh inter tmux split-window -t aurmr-inter
ssh inter tmux send-keys -t aurmr-inter:0 "activate\ aurmr_demo"  C-m
ssh inter tmux send-keys -t aurmr-inter:0 "cd\ /home/aurmr/workspaces/aurmr_demo_perception" C-m
ssh inter tmux send-keys -t aurmr-inter:0 "./simple_pick_and_stow_cli.py\ stow"
echo -n "done"
echo ""

tmux att
