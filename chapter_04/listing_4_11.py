import asyncio
import aiohttp
import logging
from util import async_timed
from chapter_04 import fetch_status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = \
            [asyncio.create_task(fetch_status(session, "https://example.com")),
             asyncio.create_task(fetch_status(session, "python://example.com"))]
        done, pending = await asyncio.wait(fetchers)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            # result = await done_task # will throw an exception
            # print(result)
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("Request got an exception",
                              exc_info=done_task.exception())

asyncio.run(main())