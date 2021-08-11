#!/bin/bash -xve

#required packages
python3 -m pip install catkin_pkg
python3 -m pip install empy
python3 -m pip install pyyaml
python3 -m pip install rospkg

cd ..
git clone https://github.com/ryuichiueda/ros_setup_scripts_Ubuntu20.04_server.git
cd ./ros_setup_scripts_Ubuntu20.04_server

bash ./step0.bash
bash ./step1.bash

#catkin_setup
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
source /opt/ros/noetic/setup.bash
catkin_init_workspace
cd ~/catkin_ws
catkin_make
