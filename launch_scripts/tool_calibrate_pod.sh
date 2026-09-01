#!/bin/bash -e


echo "Starting pod calibration"
tmux new-session -d -s aurmr-inter-calibration
tmux send-keys -t aurmr-inter-calibration:0 "activate aurmr_demo_integration_03"  C-m
tmux send-keys -t aurmr-inter-calibration:0 "rosrun aurmr_perception camera_calibration.py" C-m
echo "Move the sliders until the pod model is correctly overlaid in rviz"
echo "Then excute the other script"



sleep 1s


echo "extracing bin bounds"
echo "Please note that Nick rewrote the script"
tmux new-window -t aurmr-inter-calibration
tmux send-keys -t aurmr-inter-calibration:1 "activate aurmr_demo_integration_03"  C-m
tmux send-keys -t aurmr-inter-calibration:1 "rosrun aurmr_perception bin_bound_calculation 1"

echo "Replace 1 with the number of the Pod"





tmux att

