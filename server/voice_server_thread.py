import threading
import server.utils as utils
import subprocess


dict_msg_template = {
    "1": "Please come in",
    "2": "Please leave the package outside front door",
    "3": "Please call me this number: 123432908",
    "4": "I am at work now. Can you please come tomorrow?",
    "5": "[custom message]"
}
msg_template = sorted(dict_msg_template.items())

my_templates = "What message do you want to send?\n"
for i, info in msg_template:
    my_templates += "   ({}) {}\n".format(i, info)
my_templates += "->"

choice_str = """
What do you want to do?
    (a) Send a message to the visitor
    (b) Send a message to the visitor and then wait for response
    (c) Ignore
    (d) exit

->"""


def send_msg(conn, msg, choice=None):
    # start handshake
    if msg is None:
        msg = input("Write your message: ").strip()

    stat = utils.start_handshake_send(conn)
    if stat:
        utils.send_data(conn, msg, choice=choice)


class VoiceServer():
    def __init__(self, voice_socket=None, log=None):
        # threading.Thread.__init__(self)
        self.socket = voice_socket
        self.log = log

    def run(self):
        my_choice = input(choice_str).lower()
        self.log.info("Your choice : {}".format(my_choice))

        if my_choice in ('a', 'b'):
            my_temp_choice = input(my_templates).lower().strip()
            msg = dict_msg_template.get(my_temp_choice, None)
            if my_temp_choice == '5':
                msg = None
            send_msg(self.socket, msg, choice=my_choice)

            if my_choice == 'b':
                self.log.debug("Wait for receiving voice message")
                data = utils.recv_data(self.socket)
                print("------------")
                print("Received: \n{}\t\n".format(data))
                print("------------")
                subprocess.call("say -v Samantha '{}'".format(data))
        else:
            pass

