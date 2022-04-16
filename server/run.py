import threading as tr
from time import time
import numpy as np

import constants as const
from writer import write


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
        values = [0] * const.LAST_VALUES
        data = []
        for i in range(10000):
            distance, strength, temperature = self.sensor.read_data()
            final_time = time()
            values.pop(0)
            values.append(distance)
            data.append([final_time, distance])
            done = self.set_lanes(values, strength, final_time)
        write(data)

    def set_lanes(self, values, strength, final_time):
        values_avg = np.average(values)

        # Highest deviation
        values_std_list = [abs(ele - values_avg) for ele in values]
        values_std = np.sort(values_std_list)[0]

        # Goes through all lanes and checks if the distance is inside their lane
        for i in range(const.LANE_COUNT):
            if i not in self.lanes:
                # Check if standard deviation is too high
                if values_std < const.STANDARD_DEVIATION_MAXIMUM:
                    if i * const.LANE_WIDTH + const.LANE_OFFSET + const.LANE_TOLERANCE< values_avg < (i + 1) * const.LANE_WIDTH + const.LANE_OFFSET - const.LANE_TOLERANCE:
                        self.set_lane(i, final_time, values_avg)
        print(self.lanes, values_avg, values, values_std)

        return const.LANE_COUNT == len(self.lanes.keys())

    def set_lane(self, id, final_time, distance):
        self.lanes[id] = {
            "final_time": final_time,
            "total_time": final_time - self.start_time,
            "distance": distance,
        }
