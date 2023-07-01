import asyncio
from asyncio import Lock
from util import delay


async def a(lock: Lock):
    print("Coroutine a waiting to acquire the lock")
    async with lock:
        print("Coroutine a is in the critical section")
        await delay(2)
    print("Coroutine a released a lock")


async def b(lock: Lock):
    print("Coroutine b waiting to acquire the lock")
    async with lock:
        print("Coroutine b is in the critical section")
        await delay(2)
    print("Coroutine b released a lock")


async def main():
    lock = (
        Lock()
    )  # it tries to find event loop and make new one if none existing python <= 3.9
    await asyncio.gather(a(lock), b(lock))


asyncio.run(main())
