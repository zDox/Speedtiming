import os
import pickle
import socket
import sys
import threading as tr
path = os.path.dirname(os.path.abspath(__file__)).split("/")
path.pop(-1)
path.append("packets")
print(path)
sys.path.append("/".join(path))
import packet_types as pt
from run import Run
from sensor import Sensor

IP = socket.gethostbyname(socket.gethostname())
PORT = 6700
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = IP, PORT


class Server:
    def __init__(self):
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(ADDR)
        self.sensor = Sensor()
        self.clients = []
        self.runs = []

    def start(self):
        self.s.listen()
        print(f"\33[36;1m[LISTENING]\33[0m Server is listening on {IP}, {PORT}")

        while True:
            conn, addr = self.s.accept()
            thread = tr.Thread(target=self.hande_packet, args=(conn, addr), daemon=True)
            thread.start()
            print(f"\33[36;1m[ACTIVE CONNECTIONS]\33[0m {tr.active_count() - 1}")
            self.clients.append(conn)

    def hande_packet(self, conn, addr):
        print(f"\33[36;1m[NEW CONNECTION]\33[0m {addr} connected.")
        connected = True
        while connected:
            # receive and decode the length of the message
            buffer_length = conn.recv(HEADER).decode(FORMAT)
            if not buffer_length:
                print(f"\33[33;1m[ERROR]\33[0m Lost connection with client ({addr})")
                sys.exit()

            if buffer_length:
                action_dc = conn.recv(int(buffer_length))
                action = pickle.loads(action_dc)
                if isinstance(action, pt.Start):
                    self.runs.append(Run(1, action.start_time, self.sensor))

        conn.close()


if __name__ == '__main__':
    server = Server()
    server.start()
