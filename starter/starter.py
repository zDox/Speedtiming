import os
import random
import sys
import threading as tr

try:
    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    rpi = True
except ImportError:
    rpi = False
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
        self.starting = False
        button_thread = tr.Thread(target=self.check_button, daemon=True)
        button_thread.start()

    def start_run(self, channel):
        if not self.starting:
            self.starting = True
            status_answer = self.network_starter.ask_track_clear()
            if status_answer.status_type == "run" and status_answer.track_clear:
                for i in range(COUNTDOWN_TIME):
                    sleep(1)
                    print(COUNTDOWN_TIME - i)
                sleep(random.uniform(0, RANDOM_TIME_FACTOR))
                start_time = time()
                print("GOOO")
                start_packet = pt.Start(start_time)
                self.network_starter.sendAction(start_packet)
                self.starting = False

    def wait_start(self):
        while True:
            if not self.starting:
                if self.network_starter.handle_answer(False):
                    self.start_run("test")
                if self.check_button():
                    self.start_run("test")

    def check_button(self):
        return GPIO.input(10) == GPIO.HIGH


if __name__ == '__main__':
    starter = Starter()
    starter.wait_start()
