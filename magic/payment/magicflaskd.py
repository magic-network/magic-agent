import threading
from flask import Flask, Response, request
import asyncio

class FlaskDaemon(threading.Thread):

    def __init__(self, gateway):
        threading.Thread.__init__(self)
        self.gateway = gateway
        self.app = Flask("payment_enabler")

    def run(self):
        self.setup_routes()
        self.app.run(host='0.0.0.0')

    def keepalive(self):

        address = request.args.get('a')
        signed_message = request.args.get('s')

        asyncio.run_coroutine_threadsafe(self.gateway.on_keepalive(address, signed_message), self.gateway.loop)

        return Response(status=200)

    def get_users(self):
        return str(len(self.gateway.users.keys()))

    def setup_routes(self):
        self.add_endpoint(endpoint='/keepalive', endpoint_name='keepalive', handler=self.keepalive)
        self.add_endpoint(endpoint='/users', endpoint_name='get_users', handler=self.get_users)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, handler)
