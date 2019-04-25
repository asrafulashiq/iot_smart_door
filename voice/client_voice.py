#!/usr/bin/env python3

import socket
import time
import utils_voice as utils
import logging

import aiy.voice.tts as tts


logging.basicConfig(level=logging.DEBUG)


SERVER_IP = '192.168.1.8'
SERVER_PORT = 6500

CHUNK = 1024

choice_str = """
What do you want to do?

(a) Send a message to the visitor
(b) Send a message to the visitor and then wait for response
(c) Ignore
(d) exit
"""

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))

    logging.debug("Connected to SERVER")
    # wait for response
    while True:
        stat = utils.start_handshake_recv(client)
        if stat:
            # get the data until bye   
            recv_data, choice = utils.recv_data(client, CHUNK=CHUNK) 
            logging.info("Received data : {}".format(recv_data))
            logging.info("Choice : {}".format(choice))
            tts.say(recv_data)

            if choice == 'b':
                tts.say("Do you want any message to Ashraful?")
                voice_data = utils.voice_to_text()
                utils.send_data(client, voice_data)

        else:
            pass

    client.close()
