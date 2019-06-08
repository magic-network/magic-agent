import logging
import os
from pyrad.client import Client
from pyrad import dictionary
from pyrad import packet


class RadiusReq(object):
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        dictfile = os.path.dirname(
            os.path.realpath(__file__)) + "/raddictionary"
        self.client = Client(
            server=config['admin']['router_address'],
            secret=config['admin']['radius_secret'].encode('ascii'),
            dict=dictionary.Dictionary(dictfile))

    def sendDisconnectPacket(self, user, session):
        params = {
            'User_Name': user,
            'Acct_Session_Id': session
        }
        request = self.client.CreateCoAPacket(
            code=packet.DisconnectRequest, **params)
        result = self.client.SendPacket(request)
        if result.code != packet.DisconnectACK:
            self.logger.warning(
                'Failed to disconnect %s. Got result %s with code %d',
                user,
                result,
                result.code)
            return False
        return True


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('address')
    parser.add_argument('secret')
    parser.add_argument('user')
    parser.add_argument('session')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG)
    config = {
        'admin': {
            'router_address': args.address,
            'radius_secret': args.secret}}
    rr = RadiusReq(config)
    res = rr.sendDisconnectPacket(args.user, args.session)
    print(res)
