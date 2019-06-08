from magic.gateway.payment.types.session import SessionPaymentType


class PaymentTypeFactory:

    @staticmethod
    def createPaymentType(config):
        if config['billing']['type'] == "session":
            return SessionPaymentType(config)
        
        raise Exception("Payment type: %s not supported yet" % config['billing']['type'])
