import time
import web3
from web3 import Web3
from magic.gateway.entity.payment_channel import PaymentChannel
from magic.utils.async_tools import sync_to_async
from magic.gateway.entity.payment_type.payment_type_exception import PaymentTypeException
import aiohttp

class User():

    def __init__(self, app, radius_req, address, sessionId):

        self.app = app
        self.radius_req = radius_req
        self.address = address
        self.radiusSessionId = sessionId
        self.logger = app.logger
        self.connected = False
        self.mp_channel_id = None
        self.session_started = False
        self.session_started_at = 0
        self.last_seen_at = 0
        self.token_balance = 0

    async def get_channel(self):
        # Send off request to PE to either get

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://127.0.0.1:5000/channel', headers={'user_addr': self.address}) as resp:
                    if resp.status == 200:
                        json_body = await resp.json()
                        self.token_balance = json_body['user_balance']
        except aiohttp.client_exceptions.ClientConnectorError:
            return None


    async def payment_async(self, amount):
        # Send off request to PE to either get
        try:
            async with aiohttp.ClientSession() as session:

                body = {'payments': [{
                    "gateway_addr": self.app.addr,
                    "amount": amount
                }]}

                headers = {
                    'user_addr': self.address
                }

                async with session.post('http://127.0.0.1:5000/channel/payment', json=body, headers=headers) as resp:
                    if resp.status == 200:
                        json_body = await resp.json()
                        return True

        except aiohttp.client_exceptions.ClientConnectorError:
            return (False, 0)

    async def on_auth(self, is_new_user = False):

        self.connect()

        # send open_channel request to payment processor.
        # when approved and open, charge this user for the session.

        await self.get_channel()
        success = await self.app.payment_type.new_user_auth(self)

        return success

    def on_keepalive(self, address, signed_message):
        self.connect()


    async def on_heartbeat(self):
        
        if not self.session_started: return
        if self.connected: await self.check_timeout()

        await self.app.payment_type.heartbeat(self)

    async def check_timeout(self):

        now = time.time()
        timeout = self.app.config['dev']['user_timeout']
        elapsed = now - self.last_seen_at

        if elapsed > timeout:
            self.log("timed out. sending disconnect message to router...")
            self.disconnect()
            await self.app.payment_type.timed_out(self)


    def connect(self):
        self.last_seen_at = time.time()
        self.connected = True

    @sync_to_async
    def disconnect_async(self): return self.disconnect()
    def disconnect(self):
        # self.radius_req.sendDisconnectPacket(self.address, self.radiusSessionId)
        self.connected = False
        self.logger.warning("(%s) Disconnected." % self.address)


    @sync_to_async
    def get_token_balance_async(self): self.get_token_balance()
    def get_token_balance(self):

        try:
            balance = self.app.web3.eth.getBalance(Web3.toChecksumAddress(self.address.lower()))
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
