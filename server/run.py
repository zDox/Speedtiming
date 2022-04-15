import threading as tr
from time import time
import constants as const


class Run:
    def __init__(self, id, start_time, sensor):
        self.start_time = start_time
        self.id = id
        self.lanes = {}
        self.sensor = sensor
        thread = tr.Thread(target=self.measure, daemon=True)
        thread.start()

    def measure(self):
        done = False
        while not done:
            distance, strength, temperature = self.sensor.read_data()
            final_time = time()
            done = self.set_lanes(distance, strength, final_time)
            print(self.lanes, strength)

    def set_lanes(self, distance, strength, final_time):
        # Goes through all lanes and checks if the distance is inside their lane
        for i in range(const.LANE_COUNT):
            if i not in self.lanes and strength > 1000:
                if i * const.LANE_WIDTH + const.LANE_OFFSET < distance < (i + 1) * const.LANE_WIDTH + const.LANE_OFFSET:
                        self.set_lane(i, final_time)

        return const.LANE_COUNT == len(self.lanes.keys())

    def set_lane(self, id, final_time):
        self.lanes[id] = {
            "final_time": final_time,
            "total_time": final_time - self.start_time
        }
