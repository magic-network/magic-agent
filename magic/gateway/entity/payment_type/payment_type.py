from magic.gateway.entity.payment_type.types.session import SessionPaymentType
from magic.gateway.entity.payment_type.types.free import FreePaymentType

class PaymentTypeFactory:

    @staticmethod
    def create_payment_type(config):

        type = config['billing']['type']

        if type == "session":
            return SessionPaymentType(config)
        if type == "free":
            return FreePaymentType(config)
        else:
            raise Exception("Payment type: %s not supported yet" % type)



