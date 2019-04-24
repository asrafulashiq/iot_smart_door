#!/usr/bin/env python3
from PIL import Image
import socket
import io
import subprocess

SERVER_PORT = 6500
CHUNK = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', SERVER_PORT))

server_socket.listen()
print("The server is ready to receive")

conn, addr = server_socket.accept()
print("Connection accepted")
im_bytes = b''

while True:
    data = conn.recv(CHUNK)

    try:
        data = data.decode("utf8")
    except:
        pass

    if data.startswith("type"):
        info = str(data)
        _type = info.split(":")[-1]
        if _type == "voice":
            conn.sendall("ACK".encode("utf8"))
    elif data == "BYE":
        print("received all image bytes")

    else:
        subprocess.call("say -v Samantha 'You have a new message'",
                        shell=True)
        raise SystemExit

conn.close()
