from aiohttp import web
from magic.api import Api
from magic.payment.routes.channel import add_routes as add_channel_routes
from magic.payment.routes.admin import add_routes as add_admin_routes
from magic.payment.routes.general import add_routes as add_general_routes

class PaymentApi(Api):

    def __init__(self, app):
        super().__init__(app)
        self.decorators = Decorators(app)

        add_general_routes(self.routes, self.decorators)
        add_channel_routes(self.routes, self.decorators)
        add_admin_routes(self.routes, self.decorators)

        self.web_app.add_routes(self.routes)

class Decorators():
    def __init__(self, app):
        self.app = app

    def get_user(self, func):

        def func_wrapper(*args, **kwargs):
            request = args[0]

            try:
                kwargs['user'] = self.app.users[request.headers['user_addr']]
            except KeyError:
                kwargs['user'] = None

            return func(*args, **kwargs)

        return func_wrapper


