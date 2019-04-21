#!/usr/bin/env python3

import socket

server_port = 12000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', server_port))

server_socket.listen()
print("The server is ready to receive")

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(1024)

    # process data

    # send back data
    proc_data = data
    conn.send(proc_data)

    # close connection
    conn.close()

