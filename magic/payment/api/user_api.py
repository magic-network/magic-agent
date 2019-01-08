from aiohttp import web

def add_routes(routes, app):

    @routes.get('/ping')
    async def ping(request):
        return web.Response(text="success")

    @routes.get('/ping2')
    async def ping2(request):
        return web.Response(text="success")


