#!/usr/bin/env python3
from PIL import Image
import socket
import io
import subprocess

SERVER_PORT = 6800
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

    data_str = None
    try:
        data_str = data.decode('utf8')
    except:
        pass
    if data_str is not None:
        if data_str.startswith("type"):
            info = str(data_str)
            _type = info.split(":")[-1]
            if _type == "image":
                conn.sendall("ACK".encode("utf8"))
        elif data_str == "BYE":
            print("received all image bytes")
            image = Image.open(io.BytesIO(im_bytes))

            # notify about new visitor
            subprocess.call("say -v Samantha 'You have a new visitor'",
                            shell=True)

            image.show()
            break
        else:
            im_bytes += data
    else:
        im_bytes += data

conn.close()
