import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

address = ("127.0.0.1", 8000)
server_socket.bind(address)
server_socket.listen()
server_socket.setblocking(False)

connections = []

try:
    while True:
        connection, client_address = server_socket.accept()
        connection.setblocking(False)
        print(f"I've got a connection from {client_address}!")
        connections.append(connection)

        for connection in connections:
            buffer = b""

            while buffer[-2:] != b"\r\n":
                data = connection.recv(2)
                if not data:
                    break
                else:
                    print(f"I've got data: {data}!")
                    buffer += data
            print(f"All the data is: {buffer}")
            connection.sendall(buffer)
finally:
    server_socket.close()