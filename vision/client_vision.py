#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Camera inference face detection demo code.

Runs continuous face detection on the VisionBonnet and prints the number of
detected faces.

Example:
face_detection_camera.py --num_frames 10
"""
import argparse

from picamera import PiCamera
from time import sleep
import subprocess

from aiy.vision.inference import CameraInference, ImageInference
from aiy.vision.models import face_detection
from aiy.vision.annotator import Annotator
from io import BytesIO
from PIL import Image, ImageDraw
import datetime
import os
import glob
import sys
import logging
import socket
import argparse
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import time

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='get port')
parser.add_argument("--port", "-p", type=int, default=7000)
parser.add_argument("--ip", type=str, default='192.168.1.8')
args = parser.parse_args()

SERVER_PORT = args.port

SERVER_IP = args.ip

CHUNK = 1024


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


def get_valid_bind(start=3000, delta=50):
    cnt = 0
    while True:
        yield start + cnt * delta
        cnt += 1


def check_valid_bind(x, start=3000, delta=50):
    return (x - start) % delta == 0



def send_data(client_socket, data, type="image"):
    # initialize sending
    init_str = type.encode('utf8')

    client_socket.sendall(init_str)

    # get confirmation
    conf_dat = client_socket.recv(CHUNK)
    if conf_dat == b"ACK":
        print("Ack received from client")
        client_socket.sendall(data)
        sleep(2)
        client_socket.sendall(b"BYE")
    else:
        print("No confirmation!!!!")
    # send actual file

def get_order(client_socket):
    while True:
        conf_data = client_socket.recv(CHUNK)
        if conf_data == b"START":
            return True
        else:
            pass
        # elif conf_data == b"END":
            # return False


def main():
    """Face detection camera inference example."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_frames', '-n', type=int, dest='num_frames', default=None,
                        help='Sets the number of frames to run for, otherwise runs forever.')
    # args = parser.parse_args()

    with open("./key.key", "rb") as fp:
        key = fp.read()
    crypt = Fernet(key)

    client = connect_to_socket()

    validation_msg = crypt.encrypt(b"VISION")

    client.sendall(validation_msg)

    # Forced sensor mode, 1640x1232, full FoV. See:
    # https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes
    # This is the resolution inference run on.
    total_cam = 0
    resolution = (800, 500)
    with PiCamera(resolution=resolution, sensor_mode=4) as camera:
        camera.start_preview()
        print('Camera starting......')
        sleep(2)

        stream = BytesIO()
        inference = ImageInference(face_detection.model())

        IM_FOLDER = '/home/pi/iot/images'
        EMAIL = "ashraful31dec@gmail.com"

        i = 0

        run = get_order(client)

        while run:
            stream = BytesIO()
            detected = False
            camera.capture(stream, format='jpeg')
            print(i)
            i += 1
            stream.seek(0)
            image = Image.open(stream)
            faces = face_detection.get_faces(inference.run(image))
            if  len(faces) > 0:
                print("Found face")
                draw = ImageDraw.Draw(image)
                for face in faces:
                    x, y, width, height = face.bounding_box
                    area_ratio = (width*height)/(resolution[0]*resolution[1])
                    if area_ratio < 0.06:
                        stream.close()
                        continue
                    detected = True
                    draw.rectangle(
                        (x, y, x + width, y + height), outline='red')
                    print('Face : {}: ration : {:.2f}'.format(face, area_ratio))
                if detected:
                    now = str(datetime.datetime.now())
                    imname = IM_FOLDER + '/face_%s.jpg' % (now)
                    image.save(imname, 'JPEG')

                    stream.seek(0)
                    with stream:
                        data = stream.read()

                    # send through tcp
                    send_data(client, data, type="image")

                    subprocess.call(
                        "mpack -s 'visitor at your door' '{}' {} ".format(imname, EMAIL), shell=True)

                    run = get_order(client)
                    if not run:
                        #client.close()
                        continue

                total_cam += 1
                print('Face %d captured' % (total_cam))
            stream.close()
            sleep(0.1)

        inference.close()
        camera.stop_preview()


if __name__ == '__main__':
    main()
