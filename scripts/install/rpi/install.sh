#!/bin/bash
sudo apt-get update && \
    sudo apt-get install -yy \
        freeradius \
        freeradius-config \
        freeradius-common \
        python \
        python-dev \
        python3-dev \
        python-pip \
	build-essential \
    tk-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline6-dev \
    libdb5.3-dev \
    libgdbm-dev \
    libsqlite3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    zlib1g-dev \
    libssl-dev \
	libgmp3-dev \
	libffi6 \
	libffi-dev \
	libtool \
	autoconf \
	pkg-config \
    git

# install python 3.7 
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz | tar xf
cd Python-3.7.0
./configure
make -j 4
sudo make altinstall
cd ..
sudo rm -r Python-3.7.0
rm Python-3.7.0.tar.xz

git clone https://github.com/magic-network/magic-agent
cd magic-agent

# Set environment variables
export MAGIC_LOC=$PWD
export MAGIC_COMBINED=true
export MAGIC_SOCKPATH=/tmp/magicsock

# Required for freeradius to work
pip install future hjson

# Make comined 
sed -i "s@\"combined\": false@\"combined\": true@g" magic/gateway/default-config.hjson

# Copy all the files we actually need to run the agents
cp magic/utils/authobject.py magic/radius/authobject.py
cp magic/utils/configloader.py magic/radius/configloader.py
cp magic/gateway/default-config.hjson magic/radius/default-config.hjson
cp conf/user-config.hjson magic/radius/user-config.hjson

cp conf/user-config.hjson magic/gateway/config

# Install magic, note this installs to the python dist-packages
# thats why we need the manifest file
sudo python3.7 setup.py install

# Move the resources into place
sudo mv resources/inner-tunnel /etc/freeradius/3.0/sites-enabled/inner-tunnel
sed -i "s@MAGIC_LOC@"${MAGIC_LOC}"@g" resources/python-magic
sudo mv resources/python-magic /etc/freeradius/3.0/mods-enabled/python-magic
sudo mv resources/eap /etc/freeradius/3.0/mods-enabled/eap
sudo mv resources/clients.conf /etc/freeradius/3.0/clients.conf
sudo mv ssl/* /etc/freeradius/3.0/certs/

# Add services to startup 
sed -i "s@MAGIC_LOC@"${MAGIC_LOC}"@g" resources/services/magic.service
sed -i "s@usr/bin/python3@usr/local/bin/python3.7@g" resources/services/magic.service
sudo mv resources/services/magic.service /lib/systemd/system/magic.service
sudo mv resources/services/freeradius.service /lib/systemd/system/freeradius.service

sudo systemctl daemon-reload
sudo systemctl enable magic.service
sudo systemctl enable freeradius.service

# Remove leftover install packages
sudo apt-get --purge remove build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
sudo apt-get autoremove -y
sudo apt-get clean

#reboot to enable changes 
sudo reboot