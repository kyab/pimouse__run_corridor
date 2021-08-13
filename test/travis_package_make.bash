#!/bin/bash -xve

rsync -av ./ ~/catkin_ws/src/pimouse_run_corridor/
cd ~/catkin_ws/src
git clone https://github.com/kyab/pimouse_ros.git
cd pimouse_ros
git branch -v
git checkout master
cd ~/catkin_ws

catkin_make
