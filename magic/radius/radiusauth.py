# This is the python module called by the Radius server
# It connects to the main magic daemon and checks if the
# credentials are correct

import argparse
import logging
import socket
import os
# the files are moved into this folder when we make the radius image so 
# the linter will complain about it not being found
#pylint: disable=import-error
import radiusd
import authobject
from configloader import ConfigLoader

class RadiusAuth():
    def __init__(self):
        self.logger = logging.getLogger('RadiusAuth')
        self.load_config(os.path.dirname(os.path.realpath(__file__)))

    def load_config(self, root_folder_path):
        default_config_path = root_folder_path + '/default-config.hjson'
        user_config_path = root_folder_path + '/user-config.hjson'

        self.config = ConfigLoader()
        self.config.load(
            default_config_path=default_config_path,
            user_config_path=user_config_path)

    def authenticate(self, address, password, sess_id):
        ao = authobject.AuthObject(address, password)
        if self.config['magic']['combined']:
            client_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client_sock.connect(self.config['magic']['sockpath'])
        else:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Docker enables us to use named containers to communcate between one another, hence gateway, but can be a valid url/ip
            client_sock.connect((self.config['magic']['gateway']['location'], int(self.config['magic']['gateway']['port'])))
        client_sock.send(ao.encode())
        client_sock.shutdown(socket.SHUT_WR)
        buf = client_sock.recv(1)
        client_sock.close()
        if (buf is not None) and (buf == b'\x01'):
            return True
        return False

    def handle_radius_authorize(self, p):
        self.logger.info(repr(p))
        # This doesn't do anything right now but we could
        # use in the future to save some params about the session
        return True

    def handle_radius_authenticate(self, p):
        self.logger.info(repr(p))
        address = ''
        password = ''
        sess = ''
        for param in p:
            name = param[0]
            # We have to check the username and password because
            # there are arbitray character limits in iOS that force
            # us to switch the fields
            if name == 'User-Name':
                if '-' in param[1]:
                    password = param[1]
                else:
                    address = param[1]
            elif name == 'User-Password':
                if '-' in param[1]:
                    password = param[1]
                else:
                    address = param[1]
            elif name == 'Acct-Session-Id':
                sess = param[1]
        if not address or not password:
            self.logger.warning('No address or password sent')
            result = False
        else:
            result = self.authenticate(address, password, sess)
        return result


# Functions used by FreeRadius
def authorize(p):
    radiusd.radlog(radiusd.L_INFO, '*** magic authorize ***')
    config_logging()
    ra = RadiusAuth()
    ra.handle_radius_authorize(p)
    return (radiusd.RLM_MODULE_OK,
            tuple(),
            (
                ('Auth-Type', 'magic'),
            ))


def authenticate(p):
    radiusd.radlog(radiusd.L_INFO, '*** magic authenticate ***')
    config_logging()
    try:
        ra = RadiusAuth()
        result = ra.handle_radius_authenticate(p)
    except Exception as e:
        msg = repr(e)
        radiusd.radlog(radiusd.L_ERR, '*** ERROR:' + msg)
        return radiusd.RLM_MODULE_FAIL
    if result:
        return radiusd.RLM_MODULE_OK
    return radiusd.RLM_MODULE_REJECT
# End FreeRadius functions


def config_logging():
    logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('address')
    parser.add_argument('password')
    args = parser.parse_args()
    config_logging()
    ra = RadiusAuth()
    res = ra.authenticate(args.address, args.password, 123)
    print(res)
