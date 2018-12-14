import time
import web3
from web3 import Web3
from magic.gateway.app.payment_channel import PaymentChannel
from magic.gateway.utils.async_tools import sync_to_async
from magic.gateway.payment.payment_type_exception import PaymentTypeException

class User():

    def __init__(self, gateway, radius_req, address, sessionId):

        self.gateway = gateway
        self.radius_req = radius_req
        self.address = address
        self.radiusSessionId = sessionId
        self.logger = gateway.logger
        self.connected = False
        self.mp_channel = PaymentChannel(self, gateway)
        self.session_started = False
        self.session_started_at = 0
        self.last_seen_at = 0
        self.token_balance = 0


    async def on_auth(self, is_new_user = False):

        self.connect()

        try:

            channel_is_open = await self.check_mp_channel()

            if not channel_is_open:
                # Always get out if no payment channel is ready.
                self.end_session()
                self.disconnect()
                return False

            if is_new_user:
                await self.gateway.payment_type.new_user_auth(self)
            else:
                await self.gateway.payment_type.user_reauth(self)

            return True

        except PaymentTypeException:
            return False


    def on_keepalive(self, address, signed_message):
        self.connect()


    async def on_heartbeat(self):
        
        if not self.session_started: return
        if self.connected: await self.check_timeout()

        await self.gateway.payment_type.heartbeat(self)


    async def check_mp_channel(self):

        if self.mp_channel.is_open():
            # Check if already opened...
            return True
        else:
            # If channel isn't already opened, start a new one. only open if minimum balance in users account is met.

            await self.get_token_balance_async()
            sufficient_tokens = self.token_balance >= self.gateway.config["admin"]["user_min_balance"]

            if sufficient_tokens:
                await self.mp_channel.open()
                return True
            else:
                self.log("new user not authenticated due to not having minimum token balance: (%s/%s)." % (self.token_balance, self.gateway.config["admin"]["user_min_balance"]))
                return False


    async def check_timeout(self):

        now = time.time()
        timeout = self.gateway.config['dev']['user_timeout']
        elapsed = now - self.last_seen_at

        if elapsed > timeout:
            self.log("timed out. sending disconnect message to router...")
            self.disconnect()
            await self.gateway.payment_type.timed_out(self)


    def connect(self):
        self.last_seen_at = time.time()
        self.connected = True

    @sync_to_async
    def disconnect_async(self): return self.disconnect()
    def disconnect(self):
        self.radius_req.sendDisconnectPacket(self.address, self.radiusSessionId)
        self.connected = False
        self.logger.warning("(%s) Disconnected." % self.address)


    @sync_to_async
    def get_token_balance_async(self): self.get_token_balance()
    def get_token_balance(self):

        try:
            balance = self.gateway.web3.eth.getBalance(Web3.toChecksumAddress(self.address.lower()))
        except web3.exceptions.UnhandledRequest as e:
            print(e)

        if balance > 0:
            self.token_balance = balance

        if self.token_balance == 0:
            self.token_balance = 1000000


    def start_session(self):
        self.session_started_at = time.time()
        self.session_started = True
        self.log("New session started. ")


    def end_session(self):
        self.session_started_at = 0
        self.session_started = False


    def suspend_session(self):
        self.session_started = False


    def resume_session(self):
        self.session_started = True


    def log(self, message):
        self.logger.warning("(%s) %s" % (self.address, message))
