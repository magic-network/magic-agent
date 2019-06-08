from web3 import Web3
from magic.utils.async_tools import sync_to_async

ESCROW_AMOUNT = 10000


class PaymentChannel():

    def __init__(self, user, gateway):
        self.gateway = gateway
        self.user = user
        self.provider_balance = 0
        self.provider_escrow_balance = 0
        self.user_escrow_balance = 0
        self.id = "hologram"

    def is_open(self):
        return self.user_escrow_balance > 0

    def get_total_escrowed(self):
        return self.provider_escrow_balance + self.user_escrow_balance

    async def open(self):
        # mock out putting a chunk of the users token in escrow

        total_escrowed = self.get_total_escrowed()

        if total_escrowed == 0:
            self.user_escrow_balance += ESCROW_AMOUNT
            self.user.token_balance -= ESCROW_AMOUNT

        self.user.log(
            "Payment channel opened. Tokens escrowed: %s" %
            (self.user_escrow_balance))

    @sync_to_async
    def payment_async(self, payment): return self.payment(payment)
    def payment(self, payment):

        if self.user_escrow_balance - payment >= 0:

            self.user_escrow_balance -= payment
            self.provider_escrow_balance += payment

            return (True, None)

        else:
            return (False, "Not enough funds escrowed to continue micropayments.")

    @sync_to_async
    def settle_async(self): self.settle()
    def settle(self):

        self.provider_balance += self.provider_escrow_balance
        self.provider_escrow_balance = 0

        self.user.token_balance += self.user_escrow_balance
        self.user_escrow_balance = 0

        self.user.log(
            "user micropayment settling. User new total balance: %s " %
            self.user.token_balance)

    @sync_to_async
    def provider_payout_async(self): self.provider_payout()
    def provider_payout(self):

        # self.gateway.MgcTokenContract.functions.transfer(self.gateway.address, self.provider_escrow_balance).transact()

        self.provider_balance += self.provider_escrow_balance
        self.user.log(
            "provider channel payout: %s New balance: %s" %
            (self.provider_escrow_balance, self.provider_balance))
        self.provider_escrow_balance = 0
