import os
import random
import sys

path = os.path.dirname(os.path.abspath(__file__)).split("/")
path.pop(-1)
path.append("packets")
sys.path.append("/".join(path))
import packet_types as pt
from network_starter import NetworkStarter



from time import time, sleep

COUNTDOWN_TIME = 5
RANDOM_TIME_FACTOR = 0.4


class Starter:
    def __init__(self):
        self.network_starter = NetworkStarter()
        self.network_starter.connect_to_server()

    def start_run(self):
        for i in range(COUNTDOWN_TIME):
            sleep(1)
            print(COUNTDOWN_TIME - i)
        sleep(random.uniform(0, RANDOM_TIME_FACTOR))
        start_time = time()
        print("GOOO")
        start_packet = pt.Start(start_time)
        self.network_starter.sendAction(start_packet)

    def wait_start(self):
        while True:
            if self.network_starter.waitAction():
                self.start_run()

if __name__ == '__main__':
    starter = Starter()
    starter.wait_start()
