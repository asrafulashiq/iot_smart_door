#!/usr/bin/env python3

import socket

SERVER_IP = '192.168.1.8'
SERVER_PORT = 6800

CHUNK = 1024

def imfile_to_byte(imfile):
    with open(imfile, 'rb') as fp:
        im_data = fp.read()
        return im_data


def send_data(client_socket, data, type="image"):
    # initialize sending
    init_str = "type:{}".format(type)

    client_socket.sendall(init_str)

    # get confirmation
    conf_dat = client_socket.recv(CHUNK)
    if str(conf_dat) == "ACK":
        client_socket.sendall(data)
        client_socket.sendall("BYE")
    else:
        print("No confirmation!!!!")
    # send actual file



if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))

    imfile = '/home/pi/im.jpg'
    data = imfile_to_byte(imfile)

    # send image
    send_data(client, data, type="image")

    recv_data = client.recv(CHUNK)
    print('received data: ', recv_data)

    client.close()

