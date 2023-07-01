import asyncio
from asyncio import Queue, Task
from random import randrange
from enum import IntEnum
from dataclasses import dataclass, field
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response


routes = web.RouteTableDef()


QUEUE_KEY = "order_queue"
TASKS_KEY = "order_tasks"


class UserType(IntEnum):
    POWER_USER = 1
    NORMAL_USER = 2


@dataclass(order=True)
class Order:
    user_type: UserType
    order_delay: int = field(compare=False)


async def process_order_worker(worker_id: int, queue: Queue):
    while True:
        print(f"Worker {worker_id}: Waiting for an order...")
        order: Order = await queue.get()
        print(f"Worker {worker_id}: Processing order {order}")
        await asyncio.sleep(order.order_delay)
        print(f"Worker {worker_id}: Processed order {order}")
        queue.task_done()


@routes.post("/order")
async def place_order(request: Request) -> Response:
    body = await request.json()
    user_type = (
        UserType.POWER_USER if body["power_user"] == "True" else UserType.NORMAL_USER
    )
    order_queue = app[QUEUE_KEY]
    await order_queue.put(Order(user_type, randrange(5)))
    return Response(body="Order placed!")


async def create_order_queue(app: Application):
    print("Creating order queue and tasks.")
    queue: Queue = asyncio.Queue(10)
    app[QUEUE_KEY] = queue
    app[TASKS_KEY] = [
        asyncio.create_task(process_order_worker(i, queue)) for i in range(5)
    ]


async def destroy_queue(app: Application):
    order_tasks: list[Task] = app[TASKS_KEY]
    queue: Queue = app[QUEUE_KEY]

    print("Waiting for pending queue workers to finish...")
    try:
        await asyncio.wait_for(queue.join(), timeout=10)
    finally:
        print("Finished all pending time, canceling worker tasks...")
        [task.cancel() for task in order_tasks]


app = web.Application()
app.on_startup.append(create_order_queue)
app.on_shutdown.append(destroy_queue)

app.add_routes(routes)
web.run_app(app)
