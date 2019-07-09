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
            "gateway_balances": self.mp_channel.gateway_balance_map
        }

    @sync_to_async
    def open_channel_async(self): return self.open_channel()
    def open_channel(self):
        """Potentially opens a payment channel contingent upon blockchain status.
        """
        # check blockchain for opened channel.
        balance = self.app.mgc_channel_contract.functions.myUserBalance(self.app.payment_enabler.addr).call({'from': self.address})
        self.mp_channel.open(balance)

    @sync_to_async
    def get_user_balance_async(self): return self.get_user_balance()
    def get_user_balance(self):
        """Gets non-escrowed MGC balance of this user

        Returns:
             Number of MGC tokens
        """
        return self.app.MgcTokenContract.functions.balanceOf(self.address).call()

    @sync_to_async
    def get_user_channel_balance(self): return self.get_user_balance()
    def get_user_balance(self):
        """Gets escrowed MGC balance of this user with it's primary PE

        Returns:
             Number of escrowed MGC tokens
        """
        pass

    async def on_heartbeat(self):
        """ Called upon heartbeat tick of the main app.
        """
        pass

    def log(self, message):
        self.logger.warning("(%s) %s" % (self.address, message))