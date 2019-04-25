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


def send_msg(msg, choice=None):
    # start handshake
    if msg is None:
        msg = input("Write your message: ").strip()

    stat = utils.start_handshake_send(conn)
    if stat:
        utils.send_data(conn, msg, choice=choice)


dict_msg_template = {
    "1": "Please come in",
    "2": "Please leave the package outside front door",
    "3": "Please call me this number: 123432908",
    "4": "I am at work now. Can you please come tomorrow?",
    "5": "[custom message]"
}
msg_template = sorted(dict_msg_template.items())

my_templates = "What message do you want to send?\n"
for i, info in msg_template:
    my_templates += "   ({}) {}\n".format(i, info)
my_templates += "->"

choice_str = """
What do you want to do?
    (a) Send a message to the visitor
    (b) Send a message to the visitor and then wait for response
    (c) Ignore
    (d) exit

->"""

while True:

    my_choice = input(choice_str).lower()
    logging.info("Your choice : {}".format(my_choice))

    if my_choice in ('a', 'b'):
        my_temp_choice = input(my_templates).lower().strip()
        msg = dict_msg_template.get(my_temp_choice, None)
        send_msg(msg, choice=my_choice)
    
        if my_choice == 'b':
            logging.debug("Wait for receiving voice message")
            data = utils.recv_data(conn)
            logging.info("Received: {}\n".format(data))
    elif my_choice == 'd':
        break
    else:
        pass


conn.close()
