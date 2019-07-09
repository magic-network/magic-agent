from magic.gateway.entity.payment_type.payment_type_interface import PaymentTypeInterface

class FreePaymentType(PaymentTypeInterface):

    def __init__(self, config):
        self.config = config

    async def new_user_auth(self, user):
        return True

    async def user_reauth(self, user):
        return True

    async def heartbeat(self, user):
        pass

    async def timed_out(self, user):
        pass



