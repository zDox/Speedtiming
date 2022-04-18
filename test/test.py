import numpy as np
values = [291, 281, 243, 208, 193]
values_avg = np.average(values)
lanes = {2: {'final_time': 1650191437.727958, 'total_time': 0.003174304962158203, 'distance': 333.2}, }

# Highest deviation
values_std_list = [abs(ele - values_avg) for ele in values]
values_std = np.sort(values_std_list)[0]

for i, lane in enumerate(lanes.items()):
    print(i, lane[1])