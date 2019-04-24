#!/usr/bin/env python3
import socket
import io
import subprocess
import time
import utils
import logging

logging.basicConfig(level=logging.DEBUG)


SERVER_PORT = 6500
CHUNK = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', SERVER_PORT))

server_socket.listen()
print("The server is ready to receive")

conn, addr = server_socket.accept()
logging.info("Connection accepted")



def send_msg():

    # start handshake
    msg = input("What's your message: ")

    stat = utils.start_handshake_send(conn)
    if stat:
        utils.send_data(conn, msg)    
    

choice_str = """
What do you want to do?

(a) Send a message to the visitor
(b) Send a message to the visitor and then wait for response
(c) Ignore
(d) exit
"""

while True:

    my_choice = input(choice_str).lower()

    if my_choice == 'a':
        send_msg()
    elif my_choice == 'b':
        pass
    elif my_choice == 'd':
        break
    else:
        pass



conn.close()