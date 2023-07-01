import asyncio
import asyncpg

async def main():
    connection = await asyncpg.connect(host="localhost",
                                       port=5432,
                                       user="postgres",
                                       database="postgres",
                                       password="password")
    version = connection.get_server_version()
    print(f"Connected! Postgres version is {version}")
    await connection.close()

asyncio.run(main())