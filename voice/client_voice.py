#!/usr/bin/env python3

import socket
import time
import utils_voice as utils
import logging

import aiy.voice.tts as tts
import argparse
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken


logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='get port')
parser.add_argument("--port", "-p", type=int, default=7000)
parser.add_argument("--ip", type=str, default='192.168.1.107')
args = parser.parse_args()

SERVER_PORT = args.port

SERVER_IP = args.ip

CHUNK = 1024

with open("./key.key", "rb") as fp:
    key = fp.read()

crypt = Fernet(key)


choice_str = """
What do you want to do?

(a) Send a message to the visitor
(b) Send a message to the visitor and then wait for response
(c) Ignore
(d) exit
"""

def get_valid_bind(start=3000, delta=50):
    cnt = 0
    while True:
        yield start + cnt * delta
        cnt += 1

def check_valid_bind(x, start=3000, delta=50):
    return (x - start)%delta == 0


def connect_to_socket():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            for _port in get_valid_bind():
                try:
                    client.bind(("", _port))
                except OSError:
                    pass
                else:
                    break
            client.connect((SERVER_IP, SERVER_PORT))
            logging.debug("Connected to SERVER")
        except ConnectionRefusedError:
            logging.info("connection refused")
            time.sleep(1)
            continue
        else:
            return client

def main():
    client = connect_to_socket()
    validation_msg = crypt.encrypt(b"VOICE")
    client.sendall(validation_msg)
    # wait for response
    while True:
        try:
            stat = utils.start_handshake_recv(client)
            if stat:
                # get the data until bye
                recv_data, choice = utils.recv_data(client, CHUNK=CHUNK)
                logging.info("Received data : {}".format(recv_data))
                logging.info("Choice : {}".format(choice))
                tts.say(recv_data, volume=80)

                if choice == 'b':
                    tts.say("Do you want to send any message to Ashraful?")
                    voice_data = utils.voice_to_text()
                    utils.send_data(client, voice_data)
                    time.sleep(0.5)
            else:
                pass
        except (ConnectionRefusedError, BrokenPipeError, ConnectionResetError) as err:
            logging.error(err)
            client.close()
            main()




if __name__ == "__main__":
    main()
