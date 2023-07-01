import functools
import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor
from util import async_timed


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


@async_timed()
async def main():
    loop = asyncio.get_running_loop()
    # with ThreadPoolExecutor() as pool:
    urls = ["https://example.com" for _ in range(1000)]
    tasks = [
        loop.run_in_executor(
            None, functools.partial(get_status_code, url)
        )  # default one is ThreadPoolExecutor
        for url in urls
    ]
    results = await asyncio.gather(*tasks)
    print(results)


asyncio.run(main())
