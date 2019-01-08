from aiohttp import web
from magic.payment.entity.user import User

def add_routes(routes, decorators):

    @routes.post('/channel')
    @decorators.get_user
    async def create_channel(request, user):

        app = request.app['global']

        if user is None:
            user_id = request.headers['user_id']
            app.users[user_id] = User(app, user_id)
            return web.json_response({"success": True}, status=201)
        else:
            return web.json_response({"success": False}, status=200)



    @routes.get('/channel')
    @decorators.get_user
    async def get_channel(request, user):

        if user is not None:
            return web.json_response({"success": True, "data": user.to_response()}, status=200)
        else:
            return web.json_response({"success": False}, status=404)
