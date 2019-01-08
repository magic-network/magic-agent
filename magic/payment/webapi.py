from aiohttp import web

class WebApi():

    def __init__(self, loop):

        self.loop = loop
        self.app = web.Application(loop=loop)
        self.runner = web.AppRunner(self.app)
        self.app.add_routes([
            web.get('/ping', self.ping)
        ])

    async def run(self):
        await self.runner.setup()
        site = web.TCPSite(self.runner, '127.0.0.1', 8081)
        await site.start()

    async def ping(self, request):
        return web.Response(text="success")


