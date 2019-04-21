#!/usr/bin/env python3
from PIL import Image
import socket
import io


SERVER_PORT = 6800

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', SERVER_PORT))

server_socket.listen()
print("The server is ready to receive")

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(1024)

    # process data
    image = Image.open(io.BytesIO(data))
    image.show()
    # send back data
    proc_data = data
    conn.send(proc_data)

    # close connection
    conn.close()

