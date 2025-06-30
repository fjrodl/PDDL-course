#!/bin/bash

# File: day_2.sh
# Description: Script file for Ubuntu 24.04 jazzy
# Author: Francisco J. Rodríguez Lera (fjrodl@unileon.es)
# Date: 30/06/25
# Institution: Universidad de León

install_gz_harmonic(){
    sudo apt-get install curl
    sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y gz-harmonic
}

install_t4_robot(){
    sudo apt-get install -y ros-$ROS_DISTRO-turtlebot4-simulator
}

install_t3_robot(){
    # https://github.com/MOGI-ROS/Week-1-8-Cognitive-robotics?tab=readme-ov-file#turtlebot3-simulation

    mkdir -p turtlebot3_ws/src
    cd turtlebot3_ws/src
    git clone -b ros2 https://github.com/MOGI-ROS/turtlebot3_msgs
    git clone -b mogi-ros2 https://github.com/MOGI-ROS/turtlebot3
    git clone -b new_gazebo https://github.com/MOGI-ROS/turtlebot3_simulations

    sudo apt install -y ros-$ROS_DISTRO-dynamixel-sdk ros-$ROS_DISTRO-hardware-interface ros-$ROS_DISTRO-nav2-msgs ros-$ROS_DISTRO-nav2-costmap-2d ros-$ROS_DISTRO-nav2-map-server ros-$ROS_DISTRO-nav2-bt-navigator ros-$ROS_DISTRO-nav2-bringup ros-$ROS_DISTRO-interactive-marker-twist-server ros-$ROS_DISTRO-cartographer-ros ros-$ROS_DISTRO-slam-toolbox

    cd ..
    colcon build 
}

# variables for the installation
export pkg_dir=/home/ubuntu/pddl_ws

mkdir -p $pkg_dir/src
cd $pkg_dir/src

# Update the package list
sudo apt-get update
sudo apt-get upgrade -y

# Install Plansys 2
sudo apt install -y ros-$ROS_DISTRO-plansys2-*

# Install Turtlebot Simulator for easy example
install_gz_harmonic

install_t3_robot

# Clone the PDDL repository 
git clone https://github.com/fjrodl/PDDL-course.git


cd PDDL-course/Planners

sudo apt-get -qy install libz3-dev git g++ cmake coinor-libcbc-dev coinor-libcgl-dev coinor-libclp-dev coinor-libcoinutils-dev bison flex

#Check the environment in which you are going to compile POPF

#Environment Distro ROS 2 HUMBLE => Ubuntu 22.04, check the repository (some have humble-devel and other just humble)

git clone -b $ROS_DISTRO-devel  https://github.com/fmrico/popf.git
cd popf
mkdir build
cd build
#Remember that this is important to avoid issues with linked libraries
cmake ../ -DCMAKE_BUILD_TYPE=Release -DCMAKE_VERBOSE_MAKEFILE=TRUE
make -j
sudo make install

# Needed if you install like in this way, it is possible to compile popf with colcon
export LD_LIBRARY_PATH=/usr/local/lib/popf:$LD_LIBRARY_PATH
sudo ldconfig


cd $pkg_dir/src


# comptibility for 32 bits in ubuntu 24.04. Needed by ff.
sudo apt install -y libc6-dev-i386
 
 

# Run any additional commands or scripts as needed
echo "source $pkg_dir/install/setup.bash" >> /home/ubuntu/.bashrc
source /home/ubuntu/.bashrc

echo "================================"
echo "        DAY 3 INSTALLED         "
echo "================================"