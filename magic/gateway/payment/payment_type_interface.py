from abc import ABCMeta, abstractmethod


class PaymentTypeInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def new_user_auth(self, user):
        pass

    @abstractmethod
    def user_reauth(self, user):
        pass

    @abstractmethod
    def heartbeat(self, user):
        pass

    @abstractmethod
    def timed_out(self, user):
        pass
