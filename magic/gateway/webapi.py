from aiohttp import web

class WebApi():

    def __init__(self, loop, gateway):

        self.loop = loop
        self.gateway = gateway
        self.app = web.Application(loop=loop)
        self.runner = web.AppRunner(self.app)
        self.app.add_routes([
            web.get('/keepalive', self.keepalive),
            web.get('/users', self.get_users)
        ])

    async def run(self):
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.gateway.config['webapi']['host'], self.gateway.config['webapi']['port'])
        self.gateway.logger.warning("(WebAPI) Web api running at %s:%s" % (self.gateway.config['webapi']['host'], self.gateway.config['webapi']['port']))
        await site.start()

    async def keepalive(self, request):

        address = request.query.get('a')
        signed_message = request.query.get('s')

        await self.gateway.on_keepalive(address, signed_message)

        return web.Response(text="success")

    async def get_users(self, request):
        return web.Response(text=str(len(self.gateway.users.keys())))


