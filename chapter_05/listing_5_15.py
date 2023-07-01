import asyncio
import asyncpg

async def main():
    connection = await asyncpg.connect(host="localhost",
                                       port=5432,
                                       user="postgres",
                                       database="products",
                                       password="password")
    query = "SELECT product_id, product_name FROM product"
    async with connection.transaction():
        async for product in connection.cursor(query):
            print(product)
    
    await connection.close()

asyncio.run(main())