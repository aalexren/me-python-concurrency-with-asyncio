import asyncio
import asyncpg
from asyncpg.transaction import Transaction

import logging

async def main():
    connection = await asyncpg.connect(host="localhost",
                                       port=5432,
                                       user="postgres",
                                       database="products",
                                       password="password")
    transaction: Transaction = connection.transaction()
    await transaction.start()
    try:
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_2')")
    except asyncpg.PostgresError:
        print('Errors, rolling back transaction!')
        await transaction.rollback()
    else:
        print('No errors, committing transaction!')
        await transaction.commit()
    
    query = """SELECT brand_name FROM brand
                WHERE brand_name LIKE 'brand%'"""
    brands = await connection.fetch(query)
    print(brands)

    await connection.close()

asyncio.run(main())