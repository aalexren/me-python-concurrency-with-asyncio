import socket
import selectors
from selectors import SelectorKey

selector = selectors.DefaultSelector()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.setblocking(False)
server_socket.bind(("127.0.0.1", 8000))
server_socket.listen()

selector.register(server_socket, selectors.EVENT_READ)

while True:
    events: list[tuple[SelectorKey, int]] = selector.select(timeout=1)

    if len(events) == 0:
        print("No events, waiting a bit more!")

    for event, _ in events:
        event_socket = event.fileobj

        if event_socket == server_socket:
            connection, address = server_socket.accept()
            connection.setblocking(False)
            print(f"I've got a connection from {address}")
            selector.register(connection, selectors.EVENT_READ)
        else:
            data = event_socket.recv(1024)
            print(f"I got some data: {data}")
            event_socket.send(data)