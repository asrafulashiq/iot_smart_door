#!/usr/bin/env python3
import socket
import logging
from server.vision_server_thread import VisionServer
from server.voice_server_thread import VoiceServer
import argparse
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken


def get_valid_bind(start=3000, delta=50):
    cnt = 0
    while True:
        yield start + cnt * delta
        cnt += 1


def check_valid_bind(x, start=3000, delta=50):
    return (x - start) % delta == 0



logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='get port')
parser.add_argument("--port", "-p", type=int, default=7000)
args = parser.parse_args()

PORT = args.port
CHUNK = 1024

with open("./key.key", "rb") as fp:
    key = fp.read()

crypt = Fernet(key)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', PORT))

server_socket.listen()
print("The server is ready to receive")

conn_voice = None
conn_vision = None

while True:
    conn, addr = server_socket.accept()
    print("Connected to ", addr)
    if not check_valid_bind(addr[1]):
        logging.warning("Invalid Port\nPotential hacking from {}".format(addr))
        conn.close()
        continue
    conn.settimeout(5)
    try:
        conn_type = conn.recv(CHUNK)
    except socket.timeout:
        logging.error("Time out from {}".format(addr))
        conn.close()
        continue
    conn.settimeout(None)
    try:
        token = crypt.decrypt(conn_type)
    except InvalidToken:
        logging.warning("Invalid Token. Potential hacking from {}".format(addr))
        conn.close()
        continue
    if token == b'VISION':
        logging.info("Vision connected")
        conn_vision = conn
    elif token == b'VOICE':
        logging.info("Voice connected")
        conn_voice = conn
    else:
        logging.warning("Wrong token. Potential hacking from {}".format(addr))
        conn.close()
        print("Invalid type ", conn_type)
        continue
    if conn_vision is not None and conn_voice is not None:
        break    


while True:
    vision_thread = VisionServer(sock=conn_vision, log=logging)
    ret = vision_thread.run()
    # vision_thread.join()
    if ret:
        voice_thread = VoiceServer(voice_socket=conn, log=logging)
        voice_thread.run()
    # voice_thread.join()

conn.close()
