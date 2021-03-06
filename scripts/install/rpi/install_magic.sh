#!/bin/bash

# Build Freeradius image, currently no ARM image on dockerhub
curl -fsSL https://raw.githubusercontent.com/FreeRADIUS/freeradius-server/v3.0.x/scripts/docker/ubuntu18/Dockerfile -o Dockerfile
curl -fsSL https://raw.githubusercontent.com/FreeRADIUS/freeradius-server/v3.0.x/scripts/docker/ubuntu18/docker-entrypoint.sh -o docker-entrypoint.sh
chmod 777 ./docker-entrypoint.sh
docker build . -t freeradius

# Clone in the repo and build
git clone https://github.com/magic-network/magic-agent
cd magic-agent
sed -i "s@freeradius/freeradius-server:latest@freeradius@g" ./Dockerfile.radius
export MAGIC_LOC=$PWD
docker-compose build freeradius
# pull in the other images
docker-compose pull gateway payments

# Install the startup service
sed -i "s@MAGIC_LOC@"${MAGIC_LOC}"@g" ./resources/services/magic_docker.service
sudo mv ./resources/services/magic_docker.service /lib/systemd/system/magic.service
sudo chmod 644 /lib/systemd/system/magic.service
sudo systemctl daemon-reload
sudo systemctl enable magic.service

sudo reboot