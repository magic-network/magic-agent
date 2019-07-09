from aiohttp import web
from magic.api import Api
from magic.gateway.routes.user import add_routes as add_user_routes

class GatewayApi(Api):

    def __init__(self, app):
        super().__init__(app)
        add_user_routes(self.routes)

        self.web_app.add_routes(self.routes)
