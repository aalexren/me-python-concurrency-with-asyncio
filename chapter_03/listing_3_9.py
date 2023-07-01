import asyncio
import signal
from asyncio import AbstractEventLoop
from util import delay

"""
if execption arises during running of coroutine
we should catch it, like in this example.
simply identify these places in code by `await` statement.
"""


def cancel_task():
    print("Got a signal!")
    tasks: set[asyncio.Task] = asyncio.all_tasks()
    print(f"Cancelling {len(tasks)} task(s).")
    [task.cancel() for task in tasks]

async def main():
    loop: AbstractEventLoop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, cancel_task)

    try:
        await delay(10)
    except asyncio.CancelledError:
        print("Task is cancelled.")

asyncio.run(main())