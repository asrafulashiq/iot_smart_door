import threading
from PIL import Image
import subprocess
import io

CHUNK = 1024

class VisionServer(threading.Thread):
    def __init__(self, sock=None, log=None):
        threading.Thread.__init__(self)
        self.socket = sock
        self.log = log

    def get_decision(self):
        while True:
            decision = input(" Start monitoring? (y/n) ->").lower()
            if decision == 'y' or decision[0] == 'y':
                self.socket.sendall(b"START")
                return True
            elif decision == 'n' or decision[0] == 'n':
                self.socket.sendall(b"END")
                return False
            else:
                print("Give a valid decision (y/n)")

    def recv_image(self):
        im_bytes = b""
        while True:
            data = self.socket.recv(CHUNK)
            try:
                msg = data.decode("utf8")
                if msg.startswith("image"):
                    self.socket.sendall(b"ACK")
                elif msg.startswith("BYE"):
                    self.log.debug("received all image bytes")
                    return im_bytes
                else:
                    im_bytes += data
            except:
                im_bytes += data

    def run(self):
        decision = self.get_decision()
        if decision:
            self.log.debug("Monitoring start")
            im_bytes = self.recv_image()
            image = Image.open(io.BytesIO(im_bytes))
            # notify about new visitor
            subprocess.call("say -v Samantha 'You have a new visitor'",
                            shell=True)
            image.show()
        else:
            pass
        

