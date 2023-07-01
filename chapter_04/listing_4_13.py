import asyncio
import aiohttp
import logging
from util import async_timed
from chapter_04 import fetch_status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = \
            [asyncio.create_task(
                fetch_status(session, "https://example.com")),
             asyncio.create_task(
                fetch_status(session, "https://example.com"))]
        done, pending = await asyncio.wait(fetchers,
                                           return_when=asyncio.FIRST_COMPLETED)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            await done_task

asyncio.run(main())