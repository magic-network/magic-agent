# Magic Payment Processer Alpha
import logging
import signal
import asyncio
import json
import os
from web3 import Web3
from magic.utils.magicflaskd import FlaskDaemon
from magic.utils.configloader import ConfigLoader
from magic.utils.eth import parse_address


class MagicAgent():

    def __init__(self):
        self.logger = logging.getLogger('MagicAgent')
        self.loop = asyncio.get_event_loop()
        self.flask_daemon = FlaskDaemon(self)
        self.web3_provider = Web3.HTTPProvider(
            "https://rinkeby.infura.io/%s" %
            self.config['admin']['infura_api_key'])
        self.web3 = Web3(self.web3_provider)
        self.load_eth_contracts()
        self.shutdown = False

    def load_config(self, root_folder_path):
        default_config_path = root_folder_path + '/default-config.hjson'
        user_config_path = root_folder_path + '/user-config.hjson'

        self.config = ConfigLoader()
        self.config.load(
            default_config_path=default_config_path,
            user_config_path=user_config_path)

    def load_eth_contracts(self):

        self.mgc_contract_address = parse_address(
            self.config['dev']['mgc_address'])
        self.address = parse_address(
            self.config['admin']['eth_address'].lower())

        root_folder_path = os.path.dirname(os.path.realpath(__file__))
        mgc_abi_file = root_folder_path + '/abi/MagicToken.json'

        with open(mgc_abi_file) as f:
            info_json = json.load(f)

        self.mgc_token_contract = self.web3.eth.contract(
            address=self.mgc_contract_address,
            abi=info_json["abi"]
        )

    def sighandler(self, signum, frame):
        """
        Handle signals so that the program shuts down appropriately
        :param signum: the signal to handle
        :param frame: unused for this implementation
        """
        if signum == signal.SIGTERM:
            self.logger.warning('Got SIGTERM. Shutting down.')
            self.shutdown = True
        elif signum == signal.SIGINT:
            self.logger.warning('Got SIGINT. Shutting down.')
            self.shutdown = True
        else:
            self.logger.warning('Signal %d not handled', signum)

    def run(self):
        self.flask_daemon.daemon = True
        self.flask_daemon.start()

        try:
            self.loop.run_until_complete(self.heartbeat())
        except KeyboardInterrupt:
            self.logger.warning('Shutting down')

    async def heartbeat(self):
        # TODO: make this work in batches using asyncio.gather
        await asyncio.sleep(1)
        await self.heartbeat()
