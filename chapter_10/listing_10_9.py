import asyncio
import logging
from typing import Callable, Awaitable


class TooManyRetries(Exception):
    pass


async def retry(
    coro: Callable[[], Awaitable],
    max_retries: int,
    timeout: float,
    retry_interval: float,
):
    for retry_num in range(max_retries):
        try:
            return await asyncio.wait_for(coro(), timeout=timeout)
        except Exception as e:
            logging.exception(
                f"Exception while waiting (tried {retry_num}), retrying.", exc_info=e
            )
            await asyncio.sleep(retry_interval)
    raise TooManyRetries()
