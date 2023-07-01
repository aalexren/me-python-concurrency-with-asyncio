import asyncio
import socket
from types import TracebackType
from typing import Type

class ConnectedSocket:
    
    def __init__(self, server_socket):
        self._connection = None
        self._server_socket = server_socket

    async def __aenter__(self):
        print("Entering context manager, waiting for connection")
        loop = asyncio.get_event_loop()
        connection, address = await loop.sock_accept(self._server_socket)
        self._connection = connection
        print("Accepted a connection")
        return self._connection
    
    async def __aexit__(self,
                        exc_type: Type[BaseException] | None,
                        exc_val: BaseException | None,
                        exc_tb: TracebackType | None):
        print("Exiting context manager")
        self._connection.close() # pyright: ignore[reportOptionalMemberAccess]
        print("Closed connection")


async def main():
    loop = asyncio.get_event_loop()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", 8000))
    server_socket.setblocking(False)
    server_socket.listen()

    async with ConnectedSocket(server_socket) as connection:
        data = await loop.sock_recv(connection, 1024)
        print(data)


asyncio.run(main())