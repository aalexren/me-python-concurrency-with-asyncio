import asyncio
from asyncio import CancelledError
from util import delay


"""
`long_task` will start its execution write after
faced first `await` statement, it has not be necessary
reference to the long_task, in this exmaple
it is references to `delay(1)`. That's why we firstly
see `sleeping for 1 second` and only then
`sleeping for 10 seconds`.
"""

async def main():
    long_task = asyncio.create_task(delay(10))

    seconds_elapsed = 0

    while not long_task.done():
        print("Task not finished, cheking again in a second.")
        await delay(1)
        seconds_elapsed += 1
        if seconds_elapsed >= 5:
            long_task.cancel()
    
    try:
        await long_task
    except CancelledError:
        print("Out task was cancelled")

asyncio.run(main())