#!/usr/bin/env python3
import socket
import logging
from vision_server_thread import VisionServer

logging.basicConfig(level=logging.DEBUG)

SERVER_PORT = 7000
CHUNK = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', SERVER_PORT))

server_socket.listen()
print("The server is ready to receive")

conn, addr = server_socket.accept()
print("Connected to ", addr)

while True:
    vision_thread = VisionServer(sock=conn, log=logging)
    vision_thread.start()
    vision_thread.join()

conn.close()
