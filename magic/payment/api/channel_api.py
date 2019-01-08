from aiohttp import web

def add_routes(routes, app):

    @routes.post('/channel')
    async def create_channel(request):
        return web.Response(text="channel created!")

    @routes.get('/channel')
    async def get_channel(request):
        return web.Response(text="your channel!")

