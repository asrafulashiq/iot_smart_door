#!/usr/bin/env python3

import socket
import time

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

    data = b"You have a nw voice"
    # send image
    send_data(client, data, type="voice")

    recv_data = client.recv(CHUNK)
    print('received data: ', recv_data)

    client.close()
