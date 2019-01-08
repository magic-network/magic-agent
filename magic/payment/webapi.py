from aiohttp import web
from magic.payment.api.user_api import add_routes as add_user_routes
from magic.payment.api.channel_api import add_routes as add_channel_routes

class WebApi():

    def __init__(self, gateway):

        self.loop = gateway.loop
        self.app = web.Application(loop=self.loop)
        self.runner = web.AppRunner(self.app)
        self.routes = web.RouteTableDef()

        add_user_routes(self.routes, gateway)
        add_channel_routes(self.routes, gateway)

        self.app.add_routes(self.routes)

    async def run(self):
        await self.runner.setup()
        site = web.TCPSite(self.runner, '127.0.0.1', 8081)
        await site.start()



