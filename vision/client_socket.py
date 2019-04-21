#!/usr/bin/env python3

import socket

SERVER_IP = '192.168.1.8'
SERVER_PORT = 6800


def imfile_to_byte(imfile):
    with open(imfile, 'rb') as fp:
        im_data = fp.read()
        return im_data


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))

    imfile = '~/im.jpg'
    data = imfile_to_byte(imfile)

    client.send(data)

    recv_data = client.recv(1024)
    print('received data: ', recv_data)

    client.close()

