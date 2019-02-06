from magic.gateway.entity.payment_type.payment_type_interface import PaymentTypeInterface
import time

class SessionPaymentType(PaymentTypeInterface):

    def __init__(self, config):
        self.config = config
        self.token_per_second = int(config['billing']['charge'] / config['billing']['duration'])


    async def new_user_auth(self, user):

        total_charge = 0
        cost_to_open = self.config['billing']['cost_to_open']
        pro_rata = self.config['billing']['prorata']
        charge = self.config['billing']['charge']

        # Apply cost to open.
        total_charge += cost_to_open

        if not pro_rata:
            total_charge += charge

        if total_charge > 0:
            success = await user.payment_async(cost_to_open)

            if success:
                user.start_session()
                user.log("Charged %s token to open a new session." % total_charge)

            return success
        else:

            user.start_session()
            return True


    async def user_reauth(self, user):

        now = time.time()
        cost_to_open = self.config['billing']['cost_to_open']
        session_elapsed = now - user.session_started_at
        session_duration = self.config["billing"]["duration"]
        session_expired = session_elapsed > session_duration

        if session_expired and cost_to_open > 0:
            success = await user.payment_async(cost_to_open)
            user.start_session()
            user.log("Charged %s token to open a new session." % cost_to_open)
            return success
        else:
            user.log("User reauthed. Payment session continuing.")
            return True


    async def heartbeat(self, user):

        if self.config['billing']['prorata'] and user.connected:
            now = time.time()
            session_elapsed = now - user.session_started_at
            session_duration = self.config["billing"]["duration"]
            charge = self.token_per_second

            if session_elapsed < session_duration:
                # During the active payment session... bill continually (pro rata)

                success = await user.payment_async(charge)

                user.log("Charged %s" % charge)

                if not success:
                    # user.log(reason)
                    user.end_session()
                    await user.disconnect_async()

            else:
                user.end_session()
                await user.disconnect_async()


    async def timed_out(self, user):
        pass



