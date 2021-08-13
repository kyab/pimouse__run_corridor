#!/bin/bash -xve

rsync -av ./ ~/catkin_ws/src/pimouse_run_corridor/
cd ~/catkin_ws/src
git clone --depth=1 https://github.com/kyab/pimouse_ros.git
ls -l
cd ~/catkin_ws

catkin_make
