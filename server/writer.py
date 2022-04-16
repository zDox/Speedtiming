import csv
import os.path

fields = ["time", "distance"]


def write(data):
    for i in range(100):
        if not os.path.exists(f"data{i}.csv"):
            with open(f"data{i}.csv", "w") as file:
                csvwriter = csv.writer(file)
                csvwriter.writerow(fields)
                csvwriter.writerows(data)
            break
