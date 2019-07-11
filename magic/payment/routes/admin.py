from aiohttp import web


def add_routes(routes, decorators):

    @routes.get('/admin/users')
    async def get_channel(request):

        users = request.app['global'].users

        response = []

        for key in users:
            response.append(users[key].to_response())

        return web.json_response({"success": True, "data": response})

