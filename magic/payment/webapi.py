from aiohttp import web
from magic.payment.api.channel_api import add_routes as add_channel_routes
from magic.payment.api.admin_api import add_routes as add_admin_routes
from magic.payment.api.general_api import add_routes as add_general_routes

class WebApi():

    def __init__(self, app):

        self.loop = app.loop
        self.config = app.config
        self.logger = app.logger
        self.web_app = web.Application(loop=self.loop)
        self.web_app['global'] = app
        self.runner = web.AppRunner(self.web_app)
        self.routes = web.RouteTableDef()
        self.decorators = Decorators(app)

        add_general_routes(self.routes, self.decorators)
        add_channel_routes(self.routes, self.decorators)
        add_admin_routes(self.routes, self.decorators)

        self.web_app.add_routes(self.routes)

    async def run(self):
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.config['webapi']['host'], self.config['webapi']['port'])
        await site.start()
        self.log("(WebAPI) New API running at %s:%s" % (self.config['webapi']['host'], self.config['webapi']['port']))

    def log(self, message):
        self.logger.warning(message)

class Decorators():
    def __init__(self, app):
        self.app = app

    def get_user(self, func):

        def func_wrapper(*args, **kwargs):
            request = args[0]

            try:
                kwargs['user'] = self.app.users[request.headers['user_id']]
            except KeyError:
                kwargs['user'] = None

            return func(*args, **kwargs)

        return func_wrapper


