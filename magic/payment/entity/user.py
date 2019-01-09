from magic.payment.entity.payment_channel import PaymentChannel
from magic.utils.async_tools import sync_to_async

class User():
    def __init__(self, app, address):
        self.address = address
        self.logger = app.logger
        self.mp_channel = PaymentChannel(self, app)

    def to_response(self):
        return {
            "address": self.address,
            "user_balance": self.mp_channel.user_balance,
            "enabler_balance": self.mp_channel.enabler_balance,
            "gateway_balances": self.mp_channel.gateway_balance_map,
            "total_escrowed": self.mp_channel.get_total_escrowed()
        }

    async def on_heartbeat(self):
        pass

    def log(self, message):
        self.logger.warning("(%s) %s" % (self.address, message))