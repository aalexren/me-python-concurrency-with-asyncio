import asyncio
import asyncpg
from util import async_timed
from concurrent.futures import ProcessPoolExecutor


product_query = """
SELECT
p.product_id,
p.product_name,
p.brand_id,
s.sku_id,
pc.product_color_name,
ps.product_size_name
FROM product as p
JOIN sku as s on s.product_id = p.product_id
JOIN product_color as pc on pc.product_color_id = s.product_color_id JOIN product_size as ps on ps.product_size_id = s.product_size_id WHERE p.product_id = 100"""


async def query_product(pool: ProcessPoolExecutor):
    async with pool.acquire() as connection:
        return await connection.fetchrow(product_query)

@async_timed()
async def query_products_concurrently(pool, queries):
    queries = [query_product(pool) for _ in range(queries)]
    return await asyncio.gather(*queries)


def run_in_new_loop(num_queries: int) -> list[dict]:
    async def run_queries():
        async with asyncpg.create_pool(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="products",
            min_size=6,
            max_size=6,
        ) as pool:
            return await query_products_concurrently(pool, num_queries)

    # One thing to note here is that we convert our results into dictionaries 
    # because asyncpg record objects cannot be pickled. 
    # Converting to a data structure that is serializable ensures that 
    # we can send our result back to our parent process.
    results = [dict(result) for result in asyncio.run(run_queries())]
    return results


@async_timed()
async def main():
    loop = asyncio.get_running_loop()
    pool = ProcessPoolExecutor()
    tasks = [loop.run_in_executor(pool, run_in_new_loop, 10000) for _ in range(4)]
    all_results = await asyncio.gather(*tasks)

    total_queries = sum([len(result) for result in all_results])
    print(f"Retrieved {total_queries} products from product database.")


if __name__ == "__main__":
    asyncio.run(main())
