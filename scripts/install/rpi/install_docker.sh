#!/bin/bash
sudo apt update && sudo apt install -yy git python-pip 

# Install Docker
curl -fsSL get.docker.com -o get-docker.sh && sudo sh get-docker.sh
sudo usermod -aG docker pi
sudo apt install -yy docker-compose
sudo pip install docker-compose==1.23.2

curl -fsSL https://raw.githubusercontent.com/magic-network/magic-agent/master/scripts/install/rpi/install_magic.sh -o install_magic.sh 

sudo reboot