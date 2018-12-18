FROM ubuntu:bionic

RUN apt-get update && \
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
	pkg-config

RUN pip install future

RUN mkdir -p /home/pi/agent
ADD requirements.txt /home/pi/agent/requirements.txt

WORKDIR /home/pi/agent
RUN pip3 install -r requirements.txt

ADD . /home/pi/agent
RUN pip3 install .
ADD conf/user-config.hjson /home/pi/agent/gateway/config

ADD magic/resources/inner-tunnel /etc/freeradius/3.0/sites-enabled/inner-tunnel
ADD magic/resources/python-magic /etc/freeradius/3.0/mods-enabled/python-magic
ADD magic/resources/eap /etc/freeradius/3.0/mods-enabled/eap
ADD magic/resources/clients.conf /etc/freeradius/3.0/clients.conf

ADD run.sh /run.sh
ADD ssl/* /etc/freeradius/3.0/certs/

EXPOSE 5000/tcp 1812/udp 1813/udp

# Add Tini
ENV TINI_VERSION v0.18.0
ARG ARCH=amd64
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-${ARCH} /tini
RUN chmod +x /tini

ENTRYPOINT ["/tini", "--"]
CMD ["/run.sh", "gateway", "start"] # Set default command
