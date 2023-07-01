import socket
import logging
import asyncio
from asyncio import AbstractEventLoop

async def echo(connection: socket.socket,
               loop: AbstractEventLoop) -> None:
    try:
        while data := await loop.sock_recv(connection, 1024):
            if data == b"boom\r\n":
                raise Exception("Unexpected network error")
            await loop.sock_sendall(connection, data)
    except Exception as ex:
        logging.exception(ex)
    finally:
        connection.close()

async def listen_for_connections(server_socket: socket.socket,
                                 loop: AbstractEventLoop) -> None:
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got a connection from {address}")
        asyncio.create_task(echo(connection, loop))

async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind(("127.0.0.1", 8000))
    server_socket.setblocking(False)
    server_socket.listen()

    await listen_for_connections(server_socket, asyncio.get_event_loop())

asyncio.run(main())