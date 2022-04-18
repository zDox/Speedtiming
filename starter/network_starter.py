import sys
from os import path
import pickle
import socket
from time import sleep

path = path.dirname(path.abspath(__file__)).split("/")
path.pop(-1)
path.append("packets")
sys.path.append("/".join(path))

import packet_types as pt

PORT = 6700
FORMAT = 'utf-8'
HEADER = 64  # buffer size for header

class NetworkStarter:
    def __init__(self):
        ip = socket.gethostbyname(socket.gethostname())
        self.addr = ip, PORT  # address for socket to connect to

        self.client = socket.socket()
        self.connected = False

    def connect_to_server(self):
        i = 10
        while not self.connected:
            i -= 1
            try:
                self.client = socket.socket()
                self.client.connect(self.addr)
                self.connected = True
                break
            except socket.error:
                sleep(2)
                if i == 0:
                    break
                pass

    def sendAction(self, action, data=None):
        action_enc = pickle.dumps(action)
        buffer_length = len(action_enc)

        buffer_enc_length = str(buffer_length).encode(FORMAT)
        buffer_enc_length += b' ' * (HEADER - len(buffer_enc_length))  # fill up buffer, until it has the expected size

        self.client.send(buffer_enc_length)
        self.client.send(action_enc)
        if hasattr(action, "data_length"):
            self.client.sendall(data)

    def waitAction(self):
        # receive and decode the length of the message
        buffer_length = self.client.recv(HEADER).decode(FORMAT)
        if not buffer_length:
            exit("No Connection")
        if buffer_length:
            action_dc = self.client.recv(int(buffer_length))
            action = pickle.loads(action_dc)
            if isinstance(action, pt.StartStarter):
                return True
