from magic.gateway.payment.payment_type_interface import PaymentTypeInterface
import time

class SessionPaymentType(PaymentTypeInterface):

    def __init__(self, config):
        self.config = config
        self.token_per_second = int(config['billing']['charge'] / config['billing']['duration'])


    async def new_user_auth(self, user):

        cost_to_open = self.config['billing']['cost_to_open']

        if cost_to_open > 0:
            await user.mp_channel.payment_async(cost_to_open)
            user.start_session()
            user.log("Charged %s token to open a new session ... User escrow balance: %s" % (cost_to_open, user.mp_channel.user_escrow_balance))
        else:
            user.start_session()


    async def user_reauth(self, user):

        now = time.time()
        cost_to_open = self.config['billing']['cost_to_open']
        session_elapsed = now - user.session_started_at
        session_duration = self.config["billing"]["duration"]
        session_expired = session_elapsed > session_duration

        if session_expired and cost_to_open > 0:
            await user.mp_channel.payment_async(cost_to_open)
            user.start_session()
            user.log("Charged %s token to open a new session ... User escrow balance: %s" % (cost_to_open, user.mp_channel.user_escrow_balance))
        else:
            user.log("User reauthed. Payment session continuing.")


    async def heartbeat(self, user):

        now = time.time()
        session_elapsed = now - user.session_started_at
        session_duration = self.config["billing"]["duration"]
        charge = self.token_per_second

        if session_elapsed < session_duration:
            # During the active payment session... bill continually (pro rata)

            (success, reason) = await user.mp_channel.payment_async(charge)

            user.log("Charged %s ... User escrow balance: %s" % (charge, user.mp_channel.user_escrow_balance))

            if not success:
                user.log(reason)
                user.end_session()
                await user.mp_channel.provider_payout_async()
                await user.disconnect_async()

        else:
            user.end_session()
            await user.disconnect_async()
            await user.mp_channel.provider_payout_async()


    async def timed_out(self, user):
        pass



