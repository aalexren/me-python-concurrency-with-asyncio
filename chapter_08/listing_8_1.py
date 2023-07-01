import asyncio
from asyncio import Transport, Future, AbstractEventLoop

class HTTPGetClientProtocol(asyncio.Protocol):

    def __init__(self, host: str, loop: AbstractEventLoop):
        self._host: str = host
        self._future: Future = loop.create_future()
        self._transport: Transport | None = None
        self._response_buffer: bytes = b""

    async def get_response(self):
        return await self._future
    
    def _get_request_bytes(self) -> bytes:
        request = ("GET / HTTP/1.1\r\n"
                   "Connection: close\r\n"
                   f"Host: {self._host}\r\n\r\n")
        return request.encode()

    def connection_made(self, transport: Transport):
        print(f"Connection made to {self._host}")
        self._transport = transport
        self._transport.write(self._get_request_bytes())

    def data_received(self, data):
        print("Data received!")
        self._response_buffer += data

    def eof_received(self) -> bool | None:
        self._future.set_result(self._response_buffer.decode())
        return False
    
    def connection_lost(self, exc: Exception | None) -> None:
        if exc is None:
            print("Connection closed without error.")
        else:
            self._future.set_exception(exc)