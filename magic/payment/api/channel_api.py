from aiohttp import web
from magic.payment.entity.user import User

def add_routes(routes, decorators):

    @routes.post('/channel')
    @decorators.get_user
    async def create(request, user):

        app = request.app['global']

        if user is None:

            # This should be in a model somewhere...
            user_id = request.headers['user_id']
            new_user = User(app, user_id)
            app.users[user_id] = new_user

            body = await request.json()

            await new_user.mp_channel.create(body["escrow_amount"])

            return web.json_response({"success": True, "data": new_user.to_response()}, status=201)
        else:
            return web.json_response({"success": False}, status=200)

    @routes.get('/channel')
    @decorators.get_user
    async def get(request, user):

        if user is not None:
            return web.json_response({"success": True, "data": user.to_response()}, status=200)
        else:
            return web.json_response({"success": False}, status=404)

    @routes.post('/channel/pay')
    @decorators.get_user
    async def pay(request, user):

        body = await request.json()
        user.mp_channel.payment(body['payments'])

        return web.json_response(
            {
                "success": True,
                "data": user.to_response()
            }, status=200)

    @routes.post('/channel/topoff')
    @decorators.get_user
    async def topoff(request, user):
        user.mp_channel.topoff()
        return web.json_response({"success": True, "data": user.to_response()}, status=200)

    @routes.post('/channel/settle')
    @decorators.get_user
    async def user_settle(request, user):
        return web.json_response({"success": True, "data": user.to_response()})

