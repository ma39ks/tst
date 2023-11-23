from aiohttp import web
from config.load_all import dp, bot
from config.webhook_cfg import WEBHOOK_URL


routes = web.RouteTableDef()

@routes.get("/get_status")
async def send_ref(request):
    webhook_info = await bot.get_webhook_info()
    print(webhook_info.to_python())
    return web.Response(text="Status OK", status=200)