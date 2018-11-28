This repository contains the source code for the following magic-network services:

1. the Radius Gateway Server (to be used in conjunction with a router/AP device)
1. the Magic Provider Service.
1. the Magic Privacy Enabler Service.

The fastest way to install and run these services is to use docker.  The recommended versions are: 
1. [docker](https://www.docker.com/get-started) (18.06.1-ce+)
1. [docker-compose](https://docs.docker.com/compose/install/) (1.22.0+)

#### Want to help?
Fork, improve and PR. ;-)

---

# Radius Gateway Server    

The gateway's primary goals are to authenticate users, track usage, and charge for network usage. Any magic client user 
within range of your network may utilize your network as long as they agree with your pricing and rules.

#### Hardware & Networking:

To setup the gateway, you'll need:

1. a Router/AP device.
1. any x86 or ARM device to host the gateway server (for now)

The radius gateway server will ultimately by hosted on the network supplied by the router/AP, but we suggest 
using a pre-existing internet connection during setup. *Support for external radius gateway servers running on cloud providers such as AWS is
coming soon.*

#### Initial Setup & Run:

1. While on your gateway server device assuming a unix based system:
    ```
    git clone https://github.com/magic-network/magic-agent
    cd magic-agent
    docker-compose up -d
    ```

1. Verify the gateway is running:
    ```
    docker ps
    docker logs <container-id from output of previous command>
    ```
    
1. (optional) Stop the gateway
    ```
    docker-compose down
    ```

### Configure Router/AP:
1. Configure your router to use WPA2-Enterprise. (external guide under development)
1. Adjust gateway config with AP details and restart. (external guide under development)
1. Verify connection with the magic-cli. (external guide under development)

### Minimal Gateway Configuration:
For the gateway to run properly, you'll need to complete the config file found in the `docker-compose.yml` file 
"environments" section.

### Gateway Tests:
From `src/gateway`, run: 
```
python setup.py test
``` 

### Advanced Configuration:

The gateway server extends a default config found at `/conf/default-config.hjson`. Currently
supported options are found in the [Gateway Configuration Reference](https://www.youtube.com/watch?v=dQw4w9WgXcQ). In order 
to extend the default configuration:

1. **Extend with docker-compose.yml environment variables.** To override default config keys, specify the 
group and key separated by a underscore character, for example: ADMIN_ACCOUNT, or ADMIN_USER_MIN_BALANCE.
    ```
    services:
      magic-agent:
        build: .
        image: magic-agent
        network_mode: "host"
        ports:
          - "1812:1812/udp"
          - "1813:1813/udp"
          - "5000:5000"
        environment:
          - ADMIN_ACCOUNT=0xdf6ce563D547D56cb60FD7211061a30366D16414
          - BILLING_TYPE=session
    ```

1. **Extend with a user-config.hjson file.** Example user-config file found in `/conf/user-config.example.hjson`:

    1. Create a file named `/conf/user-config.hjson`
    1. Update with your specific settings
    1. Run `docker-compose build` on x86 machines or`docker-compose build --build-arg ARCH=armhf` on ARM machines in order
    to apply the changes.

# Payment Provider Service
Not implemented yet.

# Privacy Enabler Service
Not implemented yet.
