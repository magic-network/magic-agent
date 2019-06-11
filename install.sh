#!/bin/bash
sudo apt-get update && \
    apt-get install -yy \
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

git clone https://github.com/DomAmato/magic-agent
cd magic-agent

export MAGIC_LOC=$PWD

pip install future
pip3 install pylint

mv ./conf/user-config.hjson ./magic/gateway/config

# Install, note the when this installs it installs it to the python dist-packages
# thats why we need the manifest
pip3 install .

# Move the resources into place
mv ./magic/resources/inner-tunnel /etc/freeradius/3.0/sites-enabled/inner-tunnel
mv ./magic/resources/python-magic /etc/freeradius/3.0/mods-enabled/python-magic
sed -i "s@MAGIC_LOC@"${MAGIC_LOC}"@g" /etc/freeradius/3.0/mods-enabled/python-magic
mv ./magic/resources/eap /etc/freeradius/3.0/mods-enabled/eap
mv ./magic/resources/clients.conf /etc/freeradius/3.0/clients.conf

mv ssl/* /etc/freeradius/3.0/certs/

sed -i "s@MAGIC_LOC@"${MAGIC_LOC}"@g" ./magic.service
sudo mv ./magic.service /lib/systemd/system/magic.service

sudo reboot