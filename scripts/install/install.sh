#!/bin/bash
sudo apt-get update && \
    sudo apt-get install -yy \
        freeradius \
        freeradius-config \
        freeradius-common \
        python \
        python3 \
        python-pip \
        python3-pip \
	libssl-dev \
	libgmp3-dev \
	libffi6 \
	libffi-dev \
	libtool \
	autoconf \
	pkg-config \
    git

git clone https://github.com/magic-network/magic-agent
cd magic-agent

# Set environment variables
export MAGIC_LOC=$PWD
export MAGIC_PORT=12345
export GATEWAY_LOC=localhost

# Required for freeradius to work
pip install future

mv ./conf/user-config.hjson ./magic/gateway/config

# Install magic, note this installs to the python dist-packages
# thats why we need the manifest file
pip3 install .

# Move the resources into place
mv resources/inner-tunnel /etc/freeradius/3.0/sites-enabled/inner-tunnel
mv resources/python-magic /etc/freeradius/3.0/mods-enabled/python-magic
sed -i "s@MAGIC_LOC@"${MAGIC_LOC}"@g" /etc/freeradius/3.0/mods-enabled/python-magic
mv resources/eap /etc/freeradius/3.0/mods-enabled/eap
mv resources/clients.conf /etc/freeradius/3.0/clients.conf
mv ssl/* /etc/freeradius/3.0/certs/

# Add services to startup 
sed -i "s@MAGIC_LOC@"${MAGIC_LOC}"@g" resources/services/magic.service
sudo mv resources/services/magic.service /lib/systemd/system/magic.service
sudo mv resources/services/freeradius.service /lib/systemd/system/freeradius.service

sudo systemctl daemon-reload
sudo systemctl enable magic.service
sudo systemctl enable freeradius.service

#reboot to enable changes 
sudo reboot