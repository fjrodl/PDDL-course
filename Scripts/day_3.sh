#!/bin/bash

# File: day_3.sh
# Description: 
# Author: Francisco J. Rodríguez Lera (fjrodl@unileon.es)
# Date: 30/05/24
# Institution: Universidad de León

# variables for the installation
export pkg_dir=/home/ubuntu/pddl_ws

mkdir -p $pkg_dir/src
cd $pkg_dir/src

# Update the package list
sudo apt-get update
sudo apt-get upgrade -y

# Install Plansys 2
sudo apt install -y ros-humble-plansys2-*

# Install Turtlebot Simulator for easy example
sudo apt-get install -y ros-humble-turtlebot3*

# Clone the PDDL repository 
git clone https://github.com/fjrodl/PDDL-course.git


cd PDDL-course/Planners

sudo apt-get -qy install libz3-dev git g++ cmake coinor-libcbc-dev coinor-libcgl-dev coinor-libclp-dev coinor-libcoinutils-dev bison flex

#Check the environment in which you are going to compile POPF

#Environment Version ROS 2 HUMBLE => Ubuntu 22.04, check the repository (some have humble-devel and other just humble)

ROS_VERSION= humble-devel
git clone -b $ROS_VERSION  https://github.com/fmrico/popf.git
cd popf
mkdir build
cd build
#Remember that this is important to avoid issues with linked libraries
cmake ../ -DCMAKE_BUILD_TYPE=Release -DCMAKE_VERBOSE_MAKEFILE=TRUE
make -j
sudo make install

cd $pkg_dir/src

# Run any additional commands or scripts as needed
echo "source $pkg_dir/install/setup.bash" >> /home/ubuntu/.bashrc
source /home/ubuntu/.bashrc

echo "================================"
echo "        DAY 3 INSTALLED         "
echo "================================"
