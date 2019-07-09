from aiohttp import web


def add_routes(routes):

    @routes.get('/keepalive')
    async def keepalive(self, request):

        address = request.query.get('a')
        signed_message = request.query.get('s')

        await request.app['global'].on_keepalive(address, signed_message)

        return web.Response(text="success")

    @routes.get('/users')
    async def get_users(self, request):
        users = request.app['global'].users

        response = []

        for key in users:
            response.append(users[key].to_response())

        return web.json_response({"success": True, "data": response})