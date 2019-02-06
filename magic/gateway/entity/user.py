import time
import web3
from web3 import Web3
from magic.utils.async_tools import sync_to_async
import aiohttp

class User():

    def __init__(self, app, radius_req, address, sessionId):
        self.app = app
        self.radius_req = radius_req
        self.address = address
        self.radiusSessionId = sessionId
        self.logger = app.logger
        self.connected = False
        self.session_started = False
        self.session_started_at = 0
        self.last_seen_at = 0

    async def get_channel(self):
        # Send off request to PE to either get

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.app.config['admin']['default_penabler_url'] + '/channel', headers={'user_addr': self.address}) as resp:
                    pass
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

                async with session.post(self.app.config['admin']['default_penabler_url'] + '/channel/payment', json=body, headers=headers) as resp:
                    if resp.status == 200:
                        return True
                    else:
                        return False

        except:
            return False

    async def on_auth(self, is_new_user = False):

        self.connect()

        # send open_channel request to payment processor.
        # when approved and open, charge this user for the session.

        await self.get_channel()

        if is_new_user:
            success = await self.app.payment_type.new_user_auth(self)
        else:
            success = await self.app.payment_type.user_reauth(self)

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
