from aiohttp import web

class Api():

    def __init__(self, app):
        self.loop = app.loop
        self.config = app.config
        self.logger = app.logger
        self.web_app = web.Application(loop=self.loop)
        self.web_app['global'] = app
        self.runner = web.AppRunner(self.web_app)
        self.routes = web.RouteTableDef()

    async def run(self):
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.config['webapi']['host'], self.config['webapi']['port'])
        await site.start()
        self.log("(WebAPI) New API running at %s:%s" % (self.config['webapi']['host'], self.config['webapi']['port']))

    def log(self, message):
        self.logger.warning(message)