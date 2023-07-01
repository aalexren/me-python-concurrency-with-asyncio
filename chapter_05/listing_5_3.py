import asyncio
import asyncpg

from chapter_05.listing_5_2 import (
                                CREATE_PRODUCT_SIZE_TABLE,
                                CREATE_PRODUCT_COLOR_TABLE,
                                CREATE_BRAND_TABLE,
                                CREATE_PRODUCT_TABLE,
                                CREATE_SKU_TABLE,
                                COLOR_INSERT,
                                SIZE_INSERT
                                )

async def main():
    connection = await asyncpg.connect(host="localhost",
                                       port=5432,
                                       user="postgres",
                                       database="products",
                                       password="password")
    statements = [CREATE_BRAND_TABLE,
                  CREATE_PRODUCT_TABLE,
                  CREATE_PRODUCT_COLOR_TABLE,
                  CREATE_PRODUCT_SIZE_TABLE,
                  CREATE_SKU_TABLE,
                  SIZE_INSERT,
                  COLOR_INSERT]
    
    print("Creating the product database...")
    for statement in statements:
        status = await connection.execute(statement)
        print(status)
    print("Finished creating the product database!")
    await connection.close()

asyncio.run(main())