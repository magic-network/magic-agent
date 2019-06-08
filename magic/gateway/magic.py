# Magic Gateway Alpha
from magic.gateway.magicradiusd import RadiusDaemon
from magic.gateway.radiusreq import RadiusReq
from magic.gateway.magicflaskd import FlaskDaemon
from magic.gateway.user import User
from magic.gateway.payment.payment_type import PaymentTypeFactory
from magic.configloader import ConfigLoader
from magic.gateway.utils.eth import parse_address
import logging
import signal
import asyncio
from web3 import Web3
import json
import os


class MagicGateway():

    def __init__(self):
        self.logger = logging.getLogger('MagicGateway')
        self.config = ConfigLoader()
        self.config.load()
        self.loop = asyncio.get_event_loop()
        self.radius_daemon = RadiusDaemon(self)
        self.flask_daemon = FlaskDaemon(self)
        self.payment_type = PaymentTypeFactory.createPaymentType(self.config)
        self.radius_requester = RadiusReq(self.config)
        self.web3_provider = Web3.HTTPProvider(
            "https://rinkeby.infura.io/%s" %
            self.config['admin']['infura_api_key'])
        self.web3 = Web3(self.web3_provider)
        self.load_eth_contracts()
        self.users = {}

    def load_eth_contracts(self):

        self.mgc_contract_address = parse_address(
            self.config['dev']['mgc_address'])
        self.address = parse_address(
            self.config['admin']['eth_address'].lower())

        root_folder_path = os.path.dirname(os.path.realpath(__file__)) + "/.."
        mgc_abi_file = root_folder_path + '/abi/MagicToken.json'

        with open(mgc_abi_file) as f:
            info_json = json.load(f)

        self.MgcTokenContract = self.web3.eth.contract(
            address=self.mgc_contract_address,
            abi=info_json["abi"]
        )

    def sighandler(self, signum, frame):
        """
        Handle signals so that the program shuts down appropriately
        :param signum: the signal to handle
        :param frame: unused for this implementation
        """
        if (signum == signal.SIGTERM):
            self.logger.warning('Got SIGTERM. Shutting down.')
            self.shutdown = True
        elif (signum == signal.SIGINT):
            self.logger.warning('Got SIGINT. Shutting down.')
            self.shutdown = True
        else:
            self.logger.warning('Signal %d not handled', signum)

    def run(self):

        # may use these in the future if we want to go to a non-blocking socket
        # signal.signal(signal.SIGTERM, self.sighandler)
        # signal.signal(signal.SIGINT, self.sighandler)

        self.logger.warning(
            "Magic App Service started using eth address %s" %
            self.config['admin']['eth_address'])

        self.radius_daemon.daemon = True
        self.radius_daemon.start()
        self.flask_daemon.daemon = True
        self.flask_daemon.start()

        try:
            self.loop.run_until_complete(self.heartbeat())
        except KeyboardInterrupt:
            self.logger.warning('Shutting down')

    async def heartbeat(self):

        # TODO: make this work in batches using asyncio.gather
        for key in self.users:
            await self.users[key].on_heartbeat()

        await asyncio.sleep(1)
        await self.heartbeat()

    async def on_user_auth(self, auth_object):
        """
        Called from the flask server when a user reports in with a GET request to /keepalive
        :param auth_object: the authorization object for this user.
        """
        if auth_object.address not in self.users.keys():
            self.users[auth_object.address] = \
                User(self, address=auth_object.address,
                     sessionId=auth_object.sessionId)
            return await self.users[auth_object.address].on_auth(True)
        else:
            user = self.users[auth_object.address]
            user.radiusSessionId = auth_object.sessionId
            return await user.on_auth()

    async def on_keepalive(self, address, signed_message):
        """
        Called from the flask server when a user reports in with a GET request to /keepalive
        :param address: address name
        :param signed_message: message indicating session details sent from client
        """
        try:
            user = self.users[address]
            user.on_keepalive(address, signed_message)
        except KeyError:
            self.logger.warning(
                "Unknown user attempting keepalive. (%s)" %
                address)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    mg = MagicGateway()
    asyncio.run(mg.run(), debug=True)
