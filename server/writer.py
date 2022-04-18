import csv
import os.path


def write(name, header: [], data):
    for i in range(100):
        if not os.path.exists(f"../{name}]{i}.csv"):
            with open(f"../{name}{i}.csv", "w") as file:
                csvwriter = csv.writer(file)
                if len(data[0]) == len(header):
                    csvwriter.writerow(header)
                csvwriter.writerows(data)
            break


def write_session(treeview, runs):
    treeview_data = []
    run_header = ["time", "distance"]
    treeview_header = ["run_id", "lane_id", "total_time", "distance"]
    for run in runs:
        write("sensor_data", run_header, run.values)

    for row_id in treeview.get_children():
        row = treeview.item(row_id)["values"]
        treeview_data.append(row)
    write("run_data", treeview_header, treeview_data)
