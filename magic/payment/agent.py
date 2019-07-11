# Magic Payment Processer Alpha
import logging
import asyncio
import os
from web3 import Web3
from magic.agent import MagicAgent
from magic.utils.eth import parse_address
from magic.payment.api import PaymentApi
from magic.payment.entity.payment_enabler import PaymentEnabler

class MagicPayment(MagicAgent):

    def __init__(self):
        self.type = "payment_enabler"
        self.load_config(os.path.dirname(os.path.realpath(__file__)))
        super().__init__()
        self.logger = logging.getLogger('MagicPayment')
        self.api = PaymentApi(self)
        self.payment_enabler = PaymentEnabler(self.web3, self.mgc_token_contract, self.config)
        self.users = {}

    def run(self):
        self.logger.warning("Magic Payment Service started using eth address %s" % self.config['admin']['eth_address'])
        super().run()

    async def heartbeat(self):

        # TODO: make this work in batches using asyncio.gather
        # TODO: Add locking mechanism so long-running user processes don't get triggered twice.
        for key in self.users:
            await self.users[key].on_heartbeat()

        await super().heartbeat()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    mp = MagicPayment()
    asyncio.run(mp.run(), debug=True)
