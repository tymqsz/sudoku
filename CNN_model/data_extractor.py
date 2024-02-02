from image_processing import DigitImage
import pandas as pd  
from os import listdir, getcwd
from os.path import join, isfile
import cv2

from math import ceil

def to_csv(folder, label, size, out_file):
    cols = ["label"] + [f"pixel{x}" for x in range(784)]
    df = pd.DataFrame(columns=cols)

    index = 0
    path = join(getcwd(), folder)
    files = [f for f in listdir(path) if isfile(join(path, f))]

    multiplier = ceil(size/len(files))

    for file in files:
        img = cv2.imread(join(path, file), 0)
        flat = img.flatten().tolist()
        row = [label] + flat

        for i in range(multiplier):
            df.loc[index] = row
            index += 1

    df.to_csv(join(join(getcwd(), "data"), out_file), index=False)