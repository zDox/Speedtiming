import os.path

for i in range(100):
    print(os.path.exists(f"data{i}.csv"), i)