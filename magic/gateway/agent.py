# Magic Gateway Alpha
import logging
import asyncio
import os
from web3 import Web3
from magic.agent import MagicAgent
from magic.gateway.magicradiusd import RadiusDaemon
from magic.gateway.radiusreq import RadiusReq
from magic.gateway.user import User
from magic.gateway.payment.payment_type import PaymentTypeFactory


class MagicGateway(MagicAgent):

    def __init__(self):
        self.type = "gateway"
        self.load_config(os.path.dirname(os.path.realpath(__file__)))
        super().__init__()
        self.logger = logging.getLogger('MagicGateway')
        self.radius_daemon = RadiusDaemon(self)
        try:
            self.payment_type = PaymentTypeFactory.create_payment_type(
                self.config)
        except Exception as e:
            self.logger.warning(e)
        self.radius_requester = RadiusReq(self.config)
        self.users = {}

    def run(self):

        # may use these in the future if we want to go to a non-blocking socket
        # signal.signal(signal.SIGTERM, self.sighandler)
        # signal.signal(signal.SIGINT, self.sighandler)

        self.logger.warning(
            "Magic App Service started using eth address %s",
            self.config['admin']['eth_address'])

        self.radius_daemon.daemon = True
        self.radius_daemon.start()
        super().run()

    async def heartbeat(self):

        # TODO: make this work in batches using asyncio.gather
        for key in self.users:
            await self.users[key].on_heartbeat()

        await super().heartbeat()

    async def on_user_auth(self, auth_object):
        """
        Called from the magicradiusd daemon thread upon a successful
        verification of user's identity.
        :param auth_object: the authorization object for this user.
        """

        if auth_object.address not in self.users.keys():
            self.users[auth_object.address] = User(
                self, auth_object, auth_object.address, auth_object.sessionId)
            return await self.users[auth_object.address].on_auth(True)
        else:
            user = self.users[auth_object.address]
            user.radius_session_id = auth_object.sessionId
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
                "Unknown user attempting keepalive. (%s)",
                address)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    mg = MagicGateway()
    asyncio.run(mg.run(), debug=True)
