import asyncio
import asyncpg
from asyncpg import Connection

from random import sample
from typing import Any
from collections.abc import Coroutine

def load_common_words() -> list[str]:
    with open("chapter_05/common_words.txt") as common_words:
        return common_words.readlines()
    
def generate_brand_names(words: list[str]) -> list[tuple[str]]:
    return [(words[index],) for index in sample(range(100), 100)]

async def insert_brands(common_words: list[str],
                        connection: Connection) -> Coroutine[Any, Any, None]:
    brands = generate_brand_names(common_words)
    insert_brands = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(insert_brands, brands)

async def main():
    common_words = load_common_words()
    connection = await asyncpg.connect(host="localhost",
                                       port=5432,
                                       user="postgres",
                                       database="products",
                                       password="password")
    await insert_brands(common_words, connection)

asyncio.run(main())