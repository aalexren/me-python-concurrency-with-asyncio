import asyncio
from util import delay

async def main():
    task = asyncio.create_task(delay(10))

    try:
        result = await asyncio.wait_for(asyncio.shield(task), 2)
        print(result)
    except TimeoutError:
        print("Task took longer than five seconds, it will finish soon!")
        result = await task
        print(result)

asyncio.run(main())