import json

from aiohttp import web

app = web.Application()

class LeylaServer:
    def __init__(self, bot) -> None:
        self.bot = bot
    
    async def handle(self, request):
        return web.Response(text=json.dumps({"guilds": len(self.bot.guilds), "users": len(self.bot.users)}), status=200)

    async def run_web_server(self) -> None:
        app.router.add_get('/', self.handle)
        web.run_app(app, host='0.0.0.0', port=4014)
