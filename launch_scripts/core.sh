#!/bin/bash -e



echo "starting roscore ..."
tmux new-session -d -s aurmr-inter-core
tmux send-keys -t aurmr-inter-core:0 "activate aurmr_demo"  C-m
tmux send-keys -t aurmr-inter-core:0 "roscore" C-m

sleep 1
echo -n "done"

echo "starting azure kinect ..."
tmux new-window -t aurmr-inter-core
tmux send-keys -t aurmr-inter-core:1 "activate aurmr_demo"  C-m
tmux send-keys -t aurmr-inter-core:1 "roslaunch azure_kinect_ros_driver driver.launch point_cloud:=True" C-m
echo -n "done"

echo "starting audio capture  ..."
tmux new-window -t aurmr-inter-core
tmux send-keys -t aurmr-inter-core:2 "activate aurmr_audio"  C-m
tmux send-keys -t aurmr-inter-core:2 "roslaunch audio_capture capture.launch
" C-m
echo -n "done"



tmux att
