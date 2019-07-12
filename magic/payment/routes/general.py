from aiohttp import web

def add_routes(routes, decorators):

    @routes.get('/info')
    async def get_channel(request):
        return web.json_response(
            {
                "success": True,
                "data": {
                    "id": "magic-official",
                    "cut": .01
                }
            })

