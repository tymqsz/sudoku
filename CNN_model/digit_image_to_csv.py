import pandas as pd  
from os import listdir, getcwd
from os.path import join, isfile
import cv2

from math import ceil

# function saving image data from given folder as csv file
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

    df.to_csv(join(join(getcwd(), "CNN_model/csv_data"), out_file), index=False)


# save all digit images as csvs
#to_csv("image_data/1", 1, 1000, "1s.csv")
#to_csv("image_data/2", 2, 1000, "2s.csv")
#to_csv("image_data/3", 3, 1000, "3s.csv")
#to_csv("image_data/4", 4, 1000, "4s.csv")
#to_csv("image_data/5", 5, 1000, "5s.csv")
#to_csv("image_data/6", 6, 1000, "6s.csv")
#to_csv("image_data/7", 7, 1000, "7s.csv")
#to_csv("image_data/8", 8, 1000, "8s.csv")
to_csv("CNN_model/image_data/9", 9, 1000, "9s.csv")