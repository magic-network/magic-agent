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

# install python 3.7 
curl -fsSL https://gist.githubusercontent.com/SeppPenner/6a5a30ebc8f79936fa136c524417761d/raw/801380a7535eaf7d72e6baf9553a7b4db14c73cb/setup.sh || sh

git clone https://github.com/magic-network/magic-agent
cd magic-agent

# Set environment variables
export MAGIC_LOC=$PWD
export MAGIC_COMBINED=true
export MAGIC_SOCKPATH=/tmp/magicsock

# Required for freeradius to work
pip install future hjson

# Copy all the files we actually need to run the agents
cp magic/utils/authobject.py magic/radius/authobject.py
cp magic/utils/configloader.py magic/radius/configloader.py
cp magic/gateway/default-config.hjson magic/radius/default-config.hjson
cp conf/user-config.hjson magic/radius/user-config.hjson

cp conf/user-config.hjson magic/gateway/config

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