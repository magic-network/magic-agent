from web3 import Web3
from magic.utils.async_tools import sync_to_async


class PaymentChannel():

    def __init__(self, user, app):

        self.app = app
        self.user = user
        self.user_desired_balance = 0
        self.user_balance = 0  # Confirmed/escrowed user amount
        self.enabler_balance = 0  # The amount that the enabler has received.
        self.gateway_balance_map = {}

    def is_open(self):
        return self.user_escrow_balance > 0

    def get_total_gateway_escrowed(self):
        total_balance = 0

        for key in self.gateway_balance_map:
            total_balance += self.gateway_balance_map[key]

        return total_balance

    def get_total_escrowed(self):
        return self.user_balance + self.enabler_balance + self.get_total_gateway_escrowed()

    async def approve_transfer(self, tx_signed):
        pass

    async def create(self, tx_signed, escrow_amount):

        # For testing purposes, sign transactions here by the user, and have them submitted by the enabler.
        # self.tmp_user_privkey="8172FFF867B032376449F0D7280F6182DB6B1F1F346D514977B3819C503F6219"

        # First, check if a user has MGC in their wallet. If not, execute a signed request for airdropping!
        # user_balance = await self.user.get_user_balance_async()

        # receipt = self.app.web3.eth.sendRawTransaction(self.user.build_faucet_request_tx())

        # if (user_balance == 0):

            # self.user.log("you need airdropping!")
        signed_faucet_tx = self.user.build_faucet_request_tx()
        receipt = self.web3.eth.sendRawTransaction(signed_faucet_tx.rawTransaction)

        # else:
        #     self.user.log("you don't need airdropping! You're balance is %s" % user_balance)

        # Cache result in enabler: (eventually mysql)
        self.user_balance = escrow_amount
        self.user_desired_balance = escrow_amount

        self.user.log("Payment channel opened. Total tokens currently escrowed: %s" % escrow_amount)


    @sync_to_async
    def payment_async(self, gateway_payments): return self.payment(gateway_payments)
    def payment(self, gateway_payments):

        # gateway_payments is like this:
        # [
        #     {
        #         "gateway_addr": "123",
        #         "amount": 123
        #     }
        # ]

        total_amount = 0

        for payment in gateway_payments:
            total_amount += payment["amount"]

        if self.user_balance - total_amount >= 0:

            self.user_balance -= total_amount

            for idx, payment in enumerate(gateway_payments):

                gateway_addr = payment["gateway_addr"]
                amount = payment["amount"]

                try:
                    self.gateway_balance_map[gateway_addr] += amount
                except KeyError:
                    self.gateway_balance_map[gateway_addr] = amount

            self.user.log("User made a micropayment of %s. User new total balance: %s " % (total_amount, self.user_balance))
            return (True, None)

        else:
            self.user.log("User was unable to make a micropayment due to lack of funds.")
            return (False, "Not enough funds escrowed to continue micropayments.")


    @sync_to_async
    def topoff(self, amount=None): self.settle(amount=None)
    def topoff(self, amount=None):

        # Hit contract and transfer tokens from user to payment enabler user escrow balance
        if (amount):
            self.user_balance += amount
            self.user.log("User added balance: %s " % self.amount)
        else:
            topoff_amount = self.user_desired_balance - self.user_balance
            self.user_balance += topoff_amount
            self.user.log("User added balance: %s " % topoff_amount)

    @sync_to_async
    def settle_async(self): self.settle()
    def settle(self):

        self.user.log("user micropayment settling.")
