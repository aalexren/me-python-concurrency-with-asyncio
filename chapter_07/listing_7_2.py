import socket
from threading import Thread


class ClientEchoThread(Thread):

    def __init__(self, client):
        super().__init__()
        self.client: socket.socket = client

    def run(self):
        try:
            while True:
                data = self.client.recv(2048)
                if not data:
                    raise BrokenPipeError("Connection closed!")
                print(f"Recieved {data}, sending!")
                self.client.sendall(data)
        except OSError as e:
            print(f"Thread interrupted by {e} exception, shutting down!")
    
    def close(self):
        if self.is_alive():
            self.client.sendall(bytes("Shutting down!", encoding="utf-8"))
            self.client.shutdown(socket.SHUT_RDWR)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 8000))
    server.listen()

    connection_threads = []
    try:
        while True:
            connection, addr = server.accept()
            thread = ClientEchoThread(connection)
            connection_threads.append(thread)
            thread.start()
    except KeyboardInterrupt:
        print("Shutting down!")
        [thread.close() for thread in connection_threads]