#!/bin/bash -e


echo "Please make sure that roscore is launched using launch_aurmr_core.sh"

echo "starting robot ..."
ssh emmons tmux new-session -d -s aurmr-emmons
ssh emmons tmux send-keys -t aurmr-emmons:0 "activate\ aurmr_demo_staging"  C-m
ssh emmons tmux send-keys -t aurmr-emmons:0 "roslaunch\ tahoma_bringup\ tahoma_bringup.launch\ gui:=False\ pod_id:=1\ pod_face:=C" C-m
sleep 1
echo -n "done"
echo ""

echo "starting perception ..."
tmux new-session -d -s aurmr-inter
ssh inter tmux send-keys -t aurmr-inter:0 "activate\ aurmr_opti_grasp_rebased"  C-m
ssh inter tmux send-keys -t aurmr-inter:0 "roslaunch\ aurmr_perception\ aurmr_perception_clustering.launch\ grasp_type:=centroid" C-m
sleep 1
echo -n "done"
echo ""

echo "starting statemachine ..."
ssh emmons tmux new-window -t aurmr-emmons
ssh emmons tmux send-keys -t aurmr-emmons:1 "activate\ aurmr_demo_staging"  C-m
ssh emmons tmux send-keys -t aurmr-emmons:1 "cd\ /home/aurmr/workspaces/aurmr_demo_staging/src/aurmr_tahoma/aurmr_tasks/scripts" C-m
ssh emmons tmux send-keys -t aurmr-emmons:1 "python\ aurmr_demo"
sleep 3
ssh emmons tmux send-keys -t aurmr-emmons:1 "C-m"
echo -n "done"
echo ""


echo "starting stowing script ..."
ssh inter tmux split-window -t aurmr-inter
ssh inter tmux send-keys -t aurmr-inter:0 "activate\ aurmr_opti_grasp_rebased"  C-m
ssh inter tmux send-keys -t aurmr-inter:0 "aurmr-recorder\ new"
echo -n "done"
echo ""

tmux att
