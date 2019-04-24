import argparse
import time
import threading

from aiy.board import Board
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder

import io
import os


from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default='recording.wav')
    args = parser.parse_args()

    client = speech.SpeechClient()


    with Board() as board:
        print('Press button to start recording.')
        board.button.wait_for_press()

        done = threading.Event()
        board.button.when_pressed = done.set

        def wait():
            start = time.monotonic()
            while not done.is_set():
                duration = time.monotonic() - start
                print(
                    'Recording: %.02f seconds [Press button to stop]' % duration)
                time.sleep(0.5)

        format = AudioFormat(sample_rate_hz=44100,
                             num_channels=1, bytes_per_sample=2)
        record_file(format, filename=args.filename,
                    wait=wait, filetype='wav')
        print('Press button to play recorded sound.')
        board.button.wait_for_press()

        print('Playing...')
        play_wav(args.filename)
        print('Done.')

        # use speech to
        with io.open(args.filename, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code='en-US')
        response = client.recognize(config, audio)

        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))


if __name__ == '__main__':
    main()
