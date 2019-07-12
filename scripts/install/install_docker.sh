#!/bin/bash
sudo apt update && apt install git python-pip

# Install Docker
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker pi
sudo apt install docker-compose
sudo pip install docker-compose==1.23.2

# Clone in the repo and build
git clone https://github.com/magic-network/magic-agent
cd magic-agent
export MAGIC_LOC=$PWD
docker-compose up -d

# Install the startup service
sed -i "s@MAGIC_LOC@"${MAGIC_LOC}"@g" ./resources/services/magic_docker.service
sudo mv ./resources/services/magic_docker.service /lib/systemd/system/magic_docker.service
sudo chmod 644 /lib/systemd/system/magic.service
sudo systemctl daemon-reload
sudo systemctl enable magic.service

sudo reboot