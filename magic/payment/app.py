# Magic Gateway Alpha
from magic.configloader import ConfigLoader
from magic.utils.eth import parse_address
from magic.payment.webapi import WebApi
import logging
import signal
import asyncio
from web3 import Web3
import json
import os
import logging

class MagicPayment():

    def __init__(self):

        logging.basicConfig(level=logging.DEBUG)

        self.load_config()
        self.logger = logging.getLogger('MagicPaymentAgent')
        self.loop = asyncio.get_event_loop()
        self.web_api = WebApi(self.loop)
        self.web3_provider = Web3.HTTPProvider("https://rinkeby.infura.io/%s" % self.config['admin']['infura_api_key'])
        self.web3 = Web3(self.web3_provider)
        self.load_eth_contracts()
        self.users = {}

    def load_config(self):

        root_folder_path = os.path.dirname(os.path.realpath(__file__))
        default_config_path = root_folder_path + '/default-config.hjson'
        user_config_path = root_folder_path + '/user-config.hjson'

        self.config = ConfigLoader()
        self.config.load(default_config_path=default_config_path, user_config_path=user_config_path)


    def load_eth_contracts(self):

        self.mgc_contract_address = parse_address(self.config['dev']['mgc_address'])
        self.address = parse_address(self.config['admin']['eth_address'].lower())

        root_folder_path = os.path.dirname(os.path.realpath(__file__)) + "/.."
        mgc_abi_file = root_folder_path + '/resources/MagicToken.json'

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

        self.logger.warning("Magic Payment Service started using eth address %s" % self.config['admin']['eth_address'])

        try:
            self.loop.run_until_complete(self.start_main_loop())
        except KeyboardInterrupt:
            self.logger.warning('Shutting down')

    async def start_main_loop(self):
        await self.web_api.run()
        await self.heartbeat()

    async def heartbeat(self):

        # TODO: make this work in batches using asyncio.gather
        # TODO: Add locking mechanism so long-running user processes don't get triggered twice.
        for key in self.users:
            await self.users[key].on_heartbeat()

        await asyncio.sleep(1)
        await self.heartbeat()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    mp = MagicPayment()
    asyncio.run(mp.run(), debug=True)



