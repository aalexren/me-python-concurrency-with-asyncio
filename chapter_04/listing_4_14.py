import asyncio
import aiohttp
from util import async_timed
from chapter_04 import fetch_status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        pending = \
            [asyncio.create_task(
                fetch_status(session, "https://example.com")),
             asyncio.create_task(
                fetch_status(session, "https://example.com")),
             asyncio.create_task(
                fetch_status(session, "https://example.com"))]

        while pending:
            done, pending = await asyncio.wait(pending,
                                           return_when=asyncio.FIRST_COMPLETED)
            print(f"Done task count: {len(done)}")
            print(f"Pending task count: {len(pending)}")

            for done_task in done:
                print(await done_task)

asyncio.run(main())