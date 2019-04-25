import time
import socket
import logging

import time
import threading

from aiy.board import Board
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder

import io
import os


from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

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
    recv_data = ''
    choice = None
    while True:
        try:
            data = sock.recv(CHUNK).decode("utf8")
            if data == end_msg:
                logging.debug("All data received")
                return recv_data, choice
            elif data.startswith("CHOICE"):
                choice = data.split(":")[-1]
            else:
                recv_data += data  
        except socket.timeout:
            logging.error("No data!! Timeout!!!")
            return None
    return

def send_data(sock, data, end_msg="BYE"):
    if type(data) == str:
        data = data.encode("utf8")
    sock.sendall(data)
    time.sleep(0.5)
    sock.sendall(end_msg.encode("utf8"))
    return


def voice_to_text(filename='recording.wav'):
    client = speech.SpeechClient()

    with Board() as board:
        # logging.debug('Press button to start recording.')
        # board.button.wait_for_press()

        # done = threading.Event()
        # board.button.when_pressed = done.set

        def wait():
            start = time.monotonic()
            duration = 0
            while duration < 7: #not done.is_set():
                duration = time.monotonic() - start
                logging.debug(
                    'Recording: %.02f seconds' % duration)
                time.sleep(0.5)

        format = AudioFormat(sample_rate_hz=44100,
                             num_channels=1, bytes_per_sample=2)
        record_file(format, filename=filename,
                    wait=wait, filetype='wav')
        #logging.debug('Press button to play recorded sound.')
        #board.button.wait_for_press()

        # logging.debug('Playing...')
        # play_wav(filename)
        # logging.debug('Done.')

        # use speech to
        with io.open(filename, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code='en-US')
        response = client.recognize(config, audio)

        msg = ""
        for result in response.results:
            msg += result.alternatives[0].transcript
            logging.debug('Transcript: {}'.format(
                result.alternatives[0].transcript))
        return msg
