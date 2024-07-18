#!/bin/bash -e


echo "Starting pod calibration"
# "/home/aurmr/miniconda3/envs/aurmr_demo_integration_03/bin/python /home/aurmr/workspaces/aurmr_demo_integration_03/src/aurmr_tahoma/aurmr_perception/src/camera_calibration.py"
tmux new-session -d -s aurmr-inter-calibration
tmux send-keys -t aurmr-inter-calibration:0 "activate aurmr_demo_integration_03"  C-m
tmux send-keys -t aurmr-inter-calibration:0 "cd /home/aurmr/workspaces/aurmr_demo_integration_03/src/aurmr_tahoma/aurmr_perception/src/" C-m
tmux send-keys -t aurmr-inter-calibration:0 "python camera_calibration.py" C-m
echo "Move the sliders until the pod model is correctly overlaid in rviz"
echo "Then excute the other script"

sleep 1s


echo "extracing bin bounds"
echo "Please note that Nick rewrote the script"
# Nick rewrote the script https://raw.githubusercontent.com/au-rmr/aurmr_tahoma/nick/logging/aurmr_perception/scripts/bin_bound_calculation
# " /home/aurmr/miniconda3/envs/aurmr_demo_integration_03/bin/python /home/aurmr/workspaces/aurmr_demo_integration_03/src/aurmr_tahoma/aurmr_perception/src/pod_calibration_sub_side1.py"
tmux new-window -t aurmr-inter-calibration
tmux send-keys -t aurmr-inter-calibration:1 "activate aurmr_demo_integration_03"  C-m
tmux send-keys -t aurmr-inter-calibration:1 "cd /home/aurmr/workspaces/aurmr_demo_integration_03/src/aurmr_tahoma/aurmr_perception/src/" C-m
tmux send-keys -t aurmr-inter-calibration:1 " python pod_calibration_sub_side1.py" 





tmux att

