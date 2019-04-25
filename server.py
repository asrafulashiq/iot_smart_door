#!/usr/bin/env python3
import socket
import logging
from server.vision_server_thread import VisionServer
from server.voice_server_thread import VoiceServer
import argparse

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='get port')
parser.add_argument("--port", "-p", type=int, default=7000)
args = parser.parse_args()

PORT = args.port
CHUNK = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', PORT))

server_socket.listen()
print("The server is ready to receive")

conn_voice = None
conn_vision = None

while True:
    conn, addr = server_socket.accept()
    print("Connected to ", addr)
    conn_type = conn.recv(CHUNK)
    if conn_type == b'VISION':
        logging.info("Vision connected")
        conn_vision = conn
    elif conn_type == b'VOICE':
        logging.info("Voice connected")
        conn_voice = conn
    else:
        print("Invalid type ", conn_type)
    if conn_vision is not None and conn_voice is not None:
        break    


while True:
    vision_thread = VisionServer(sock=conn_vision, log=logging)
    vision_thread.run()
    # vision_thread.join()

    voice_thread = VoiceServer(voice_socket=conn, log=logging)
    voice_thread.run()
    # voice_thread.join()

conn.close()
