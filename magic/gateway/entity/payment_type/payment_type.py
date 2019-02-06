from magic.gateway.entity.payment_type.types.session import SessionPaymentType
from magic.gateway.entity.payment_type.types.free import FreePaymentType

class PaymentTypeFactory:

    @staticmethod
    def createPaymentType(config):

        type = config['billing']['type']

        if type == "session":
            return SessionPaymentType(config)
        if type == "free":
            return FreePaymentType(config)
        else:
            message = "Payment type: %s not supported yet" % type
            gateway.logger.warning(message)
            raise Exception(message)



