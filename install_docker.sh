#!/bin/bash
sudo apt update
sudo apt install git
sudo apt install python-pip

curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker pi
sudo apt install docker-compose
sudo pip install docker-compose==1.23.2

git clone https://github.com/magic-network/magic-agent
cd magic-agent
docker-compose up -d

sudo mv ./magic_docker.service /lib/systemd/system/magic.service
sudo chmod 644 /lib/systemd/system/magic.service
sudo systemctl daemon-reload
sudo systemctl enable magic.service

sudo reboot