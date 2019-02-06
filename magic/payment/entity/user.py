from magic.payment.entity.payment_channel import PaymentChannel
from magic.utils.async_tools import sync_to_async

class User():
    def __init__(self, app, address):
        self.address = address
        self.logger = app.logger
        self.app = app
        self.mp_channel = PaymentChannel(self, app)

    def to_response(self):
        return {
            "address": self.address,
            "user_balance": self.mp_channel.user_balance,
            "enabler_balance": self.mp_channel.enabler_balance,
            "gateway_balances": self.mp_channel.gateway_balance_map,
            "total_escrowed": self.mp_channel.get_total_escrowed()
        }

    @sync_to_async
    def open_channel_async(self): return self.open_channel()
    def open_channel(self):
        # check blockchain for opened channel.
        balance = self.app.mgc_channel_contract.functions.myUserBalance(self.app.payment_enabler.addr).call({'from': self.address})
        self.mp_channel.activate(balance)

    @sync_to_async
    def get_user_balance_async(self): return self.get_user_balance()
    def get_user_balance(self):
        return self.app.MgcTokenContract.functions.balanceOf(self.address).call()

    @sync_to_async
    def get_user_channel_balance(self): return self.get_user_balance()
    def get_user_balance(self):
        return self.app.MgcTokenContract.functions.balanceOf(self.address).call()

    def build_faucet_request_tx(self):

        priv_key = "8172FFF867B032376449F0D7280F6182DB6B1F1F346D514977B3819C503F6219"

        nonce = self.app.web3.eth.getTransactionCount(self.address)

        request_tx = self.app.MgcTokenFaucetContract.functions.request().buildTransaction({
            'chainId': 4,
            'gas': 70000,
            'gasPrice': self.app.web3.toWei('1', 'gwei'),
            'nonce': nonce
        })

        signed_request_tx = self.app.web3.eth.account.signTransaction(request_tx, private_key=priv_key)

        return signed_request_tx


    def build_approve_channels_tx(self):
        return "hi"

    def build_open_channel_tx(self):
        return "hi"

    async def on_heartbeat(self):
        pass

    def log(self, message):
        self.logger.warning("(%s) %s" % (self.address, message))