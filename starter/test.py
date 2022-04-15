import os

path = os.path.dirname(os.path.abspath(__file__)).split("/")
path.pop(-1)
path.append("packets")
print("/".join(path))