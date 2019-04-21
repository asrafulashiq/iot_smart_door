#!/usr/bin/env python3

import socket

SERVER_IP = '192.168.1.8'
SERVER_PORT = 12000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

data = "Hello"

client.send(data.encode("utf8"))

recv_data = client.recv(1024)

client.close()

