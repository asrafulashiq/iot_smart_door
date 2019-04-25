#!/usr/bin/env python3
import socket
import io
import subprocess
import time
import utils
import logging
from voice_server_thread import VoiceServer

logging.basicConfig(level=logging.DEBUG)


SERVER_PORT = 6800
CHUNK = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', SERVER_PORT))

server_socket.listen()
print("The server is ready to receive")

conn, addr = server_socket.accept()
logging.info("Connection established with {}".format(addr))

while True:
    voice_thread = VoiceServer(voice_socket=conn, log=logging)
    voice_thread.start()
    voice_thread.join()
    logging.debug("Starting new voice Thread")