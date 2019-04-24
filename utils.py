import time
import socket
import logging

logging.basicConfig(level=logging.DEBUG)


def start_handshake_send(sock, init_str="INIT", CHUNK=1024):
    data = init_str.encode("utf8")
    sock.sendall(data)

    try:
        msg = sock.recv(CHUNK)
        if msg == b"ACK":
            logging.debug("Ready to send data")
            return True
    except socket.timeout:
        logging.error("Acknowledge time out!!! Try again!!!")
        return False
    return False

def start_handshake_recv(sock, init_str="INIT", CHUNK=1024):
    try:
        msg = sock.recv(CHUNK)
        if msg == init_str.encode("utf8"):
            logging.debug("handshake initiated. Ready to get msg.")
            sock.sendall(b"ACK")
            return True
    except socket.timeout:
        logging.error("No hadnshake initialization from server")
        return False
    

def recv_data(sock, end_msg="BYE", CHUNK=1024):
    recv_data = b''
    while True:
        try:
            data = sock.recv(CHUNK)
            if data == end_msg.encode('utf8'):
                logging.debug("All data received")
                return data
            else:
                recv_data += data  
        except socket.timeout:
            logging.error("No data!! Timeout!!!")
            return None


def send_data(sock, data, end_msg="BYE"):
    if type(data) == str:
        data = data.encode("utf8")
    sock.sendall(data)
    time.sleep(0.5)
    sock.sendall(end_msg.encode("utf8"))
    return


