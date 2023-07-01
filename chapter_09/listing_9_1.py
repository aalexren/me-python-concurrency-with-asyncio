from aiohttp import web
from datetime import datetime
from aiohttp.web_request import Request
from aiohttp.web_response import Response

routes = web.RouteTableDef()

@routes.get("/time")
async def time(request: Request) -> Response:
    today = datetime.today()

    result = {
        "month": today.month,
        "day": today.day,
        "time": str(today.time()),
    }

    return web.json_response(result)

app = web.Application()
app.add_routes(routes)
web.run_app(app)