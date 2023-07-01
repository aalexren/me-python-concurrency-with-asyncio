import asyncpg
from asyncpg import Record
from asyncpg.pool import Pool

from aiohttp import web
from aiohttp.web import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response

routes = web.RouteTableDef()
DB_KEY = "database"


async def create_database_pool(app: Application):
    print("Creating database pool.")
    pool: Pool = await asyncpg.create_pool(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        password="password",
        database="products",
        min_size=6,
        max_size=6,
    )
    app[DB_KEY] = pool


async def destroy_database_pool(app: Application):
    print("CLosing database pool.")
    pool: Pool = app[DB_KEY]
    await pool.close()


@routes.get("/brands")
async def time(request: Request) -> Response:
    connection: Pool = request.app[DB_KEY]
    brand_query = "SELECT brand_id, brand_name FROM brand"
    results: list[Record] = await connection.fetch(brand_query)
    result_as_dict: list[dict] = [dict(brand) for brand in results]
    return web.json_response(result_as_dict)



if __name__ == "__main__":
    app = web.Application()
    app.on_startup.append(create_database_pool)
    app.on_cleanup.append(destroy_database_pool)

    app.add_routes(routes)
    web.run_app(app, host="localhost")
