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
            "user_escrow_balance": self.mp_channel.user_escrow_balance
        }

    async def on_heartbeat(self):
        pass