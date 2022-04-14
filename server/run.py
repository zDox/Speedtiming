import threading as tr
from time import time


class Run:
    def __init__(self, id, start_time, sensor):
        self.start_time = start_time
        self.id = id
        self.lanes = {}
        self.sensor = sensor
        thread = tr.Thread(target=self.measure, daemon=True)
        thread.start()

    def measure(self):
        while True:
            distance, strength, temperature = self.sensor.read_data()
            if 30 < distance < 60:
                self.set_lane(1, time())

    def set_lane(self, id, final_time):
        self.lanes[id] = {
            "final_time": final_time,
            "total_time": final_time - self.start_time
        }
