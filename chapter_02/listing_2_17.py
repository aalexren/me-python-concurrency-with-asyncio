import asyncio
from util import async_timed, delay

@async_timed()
async def delay(delay_seconds: int) -> int:
    print(f"sleeping for {delay_seconds} second(s)")
    await asyncio.sleep(delay_seconds)
    print(f"finished sleeping for {delay_seconds} second(s)")
    return delay_seconds

@async_timed()
async def main():
    task_one = asyncio.create_task(delay(2))
    task_two = asyncio.create_task(delay(3))

    await delay(5)
    print(task_one, task_two) # tasks are done but 
                              # we need `await` them to get result

    await task_one
    await task_two


asyncio.run(main())