import asyncio
from aiohttp import ClientSession
from util import async_timed, delay

@async_timed()
async def fetch_status(session: ClientSession,
                       url: str,
                       delay_seconds: int=0) -> int:
    if delay_seconds:
        await delay(delay_seconds)
    async with session.get(url) as result:
        return result.status
    
@async_timed()
async def main():
    async with ClientSession() as session:
        url = "https://example.com"
        status = await fetch_status(session, url)
        print(f"Status for {url} was {status}")

if __name__ == "__main__":
    asyncio.run(main())