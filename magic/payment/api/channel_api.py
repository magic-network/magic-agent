from aiohttp import web
from magic.payment.entity.user import User
from magic.payment.entity.payment_channel import PaymentChannel
from magic.utils.eth import verify_sig

def add_routes(routes, decorators):

    @routes.post('/airdrop')
    async def airdrop(request):

        app = request.app['global']
        body = await request.json()
        verified = verify_sig("it's me!", body['sig'], body['address'])

        if verified:
            (token_receipt, eth_receipt) = await app.payment_enabler.airdrop(body['address'])
            return web.json_response({
                "success": True,
                "token_receipt": token_receipt.hex(),
                "eth_receipt": eth_receipt.hex()
            }, status=200)
        else:
            return web.json_response({
                "success": False,
                "error": "Do we know you?? body.sig did not validate."
            }, status=401)


    @routes.post('/channel')
    @decorators.get_user
    async def create(request, user):

        app = request.app['global']

        if user is None:

            # This should be in a model somewhere...
            user_addr = request.headers['user_addr']
            new_user = User(app, user_addr)
            app.users[user_addr] = new_user

            body = await request.json()

            await new_user.mp_channel.create(body["escrow"])

            return web.json_response({"success": True, "data": new_user.to_response()}, status=201)
        else:
            return web.json_response({"success": False}, status=200)

    @routes.get('/channel')
    @decorators.get_user
    async def get(request, user):

        app = request.app['global']

        if user is not None:
            return web.json_response({"success": True, "channel_id": 123}, status=200)
        else:

            user_addr = request.headers['user_addr']
            new_user = User(app, user_addr)
            app.users[user_addr] = new_user
            await new_user.open_channel_async()

            if new_user.mp_channel.activated:
                return web.json_response({"success": True, "user_balance": new_user.mp_channel.user_balance}, status=200)
            else:
                return web.json_response({"success": False}, status=200)

    @routes.post('/channel/payment')
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

