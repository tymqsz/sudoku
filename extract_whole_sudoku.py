import shutil
import os

labels = [
    0, 0, 0, 1, 6, 0, 0, 0, 5,
    1, 2, 0, 0, 3, 5, 0, 0, 0,
    0, 0, 6, 0, 0, 0, 0, 9, 0,
    9, 8, 2, 4, 1, 0, 5, 0, 7,
    0, 0, 0, 0, 0, 2, 4, 0, 9,
    0, 1, 5, 3, 7, 9, 6, 0, 8,
    6, 9, 0, 7, 0, 0, 0, 5, 0,
    0, 4, 1, 0, 0, 0, 0, 7, 2,
    0, 0, 0, 0, 0, 3, 0, 0, 1
]


for i in range(81):
    if labels[i] == 0:
        continue

    source = f"tiles/tile{i}.jpg"
    dir = f"sudata/{labels[i]}/"
    f_count = len([entry for entry in os.listdir(dir) if os.path.isfile(os.path.join(dir, entry))])
    dest = f"{dir}tile{f_count}.jpg"

    shutil.copyfile(source, dest)