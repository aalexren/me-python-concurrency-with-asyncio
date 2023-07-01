import asyncio
from util import async_timed, delay

"""
but we're still trapped in last comprehension.
even this would run in around 3 seconds
we couldn't run any another code till
all tasks are awaited in this comprehension!
"""

@async_timed()
async def main():
    delay_times = [3, 3, 3]
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    [await task for task in tasks] # halting

asyncio.run(main())