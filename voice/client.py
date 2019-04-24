#!/usr/bin/env python3

import socket
import time
import utils
import logging

logging.basicConfig(level=logging.DEBUG)


SERVER_IP = '192.168.1.8'
SERVER_PORT = 6500

CHUNK = 1024


def send_data(client_socket, data, type="image"):
    # initialize sending
    init_str = ("type:{}".format(type)).encode('utf8')

    client_socket.sendall(init_str)

    # get confirmation
    conf_dat = client_socket.recv(CHUNK)
    if conf_dat == "ACK".encode('utf8'):
        print("Ack received from client")
        client_socket.sendall(data)
        time.sleep(2)
        client_socket.sendall("BYE".encode('utf8'))
    else:
        print("No confirmation!!!!")
    # send actual file


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))

    # wait for response
    while True:
        stat = utils.start_handshake_recv(client)
        if stat:
            # get the data until bye   
            recv_data = utils.recv_data(client, CHUNK=CHUNK) 
            recv_data = recv_data.decode("utf8")
            logging.info("Received data : {}".format(recv_data))
        else:
            pass

    client.close()
