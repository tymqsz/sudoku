from image_processing import DigitImage
from PIL import Image
import cv2
import numpy as np
from conv import transform
from data_extractor import to_csv
import os


folders = ["1", "9"]

kernels = [ np.array([[1.05, 0, 0],
                       [0, 1.05, 0],
                       [0, 0, 1]]), 

            np.array([[0.95, 0, 0],
                       [0, 0.95, 0],
                       [0, 0, 1]]), 
           
            np.array([  [1/9, 1/9, 1/9],
                        [1/9, 1/9, 1/9],
                        [1/9, 1/9, 1/9] ]),

            np.array([  [0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]
])]

for folder in folders:
    files = [f for f in os.listdir(os.path.join(os.getcwd(), folder))]
    for file in files:
        source = folder+"/"+file
        image = cv2.imread(source, 0)

        f_image = Image.fromarray(image, "L")
        f_image.save(source)

        i = 0
        for kernel in kernels:
            transformed = transform(kernel, f_image)
            f = file.split(".")[0] + f"{i}.png"
            transformed.save(f"{folder}/{f}")
            i += 1

