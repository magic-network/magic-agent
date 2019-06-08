# Magic Payment Processer Alpha
import logging
import asyncio
import os
from magic.agent import MagicAgent
from web3 import Web3


class MagicPayment(MagicAgent):

    def __init__(self):
        self.type = "payment_enabler"
        self.load_config(os.path.dirname(os.path.realpath(__file__)))
        super().__init__()
        self.logger = logging.getLogger('MagicPayment')

    def run(self):

        self.logger.warning("Magic Payment Enabler started.")

        super().run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    mp = MagicPayment()
    asyncio.run(mp.run(), debug=True)
