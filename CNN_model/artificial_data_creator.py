from PIL import Image
import cv2
import numpy as np
from convolution import transform
import os

# folders which contain digit images extracted from sudokus 
folders = ["image_data/"+str(x) for x in range(1, 10)]


# basic convolution kernels used to create some noise in images
kernels = [ np.array([[1.05, 0, 0],
                       [0, 1.05, 0],
                       [0, 0, 1]]), 

            np.array([[0.95, 0, 0],
                       [0, 0.95, 0],
                       [0, 0, 1]]), 
           
            np.array([[1/9, 1/9, 1/9],
                        [1/9, 1/9, 1/9],
                        [1/9, 1/9, 1/9]]),

            np.array([[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]]) ]


for folder in folders:
    files = [f for f in os.listdir(os.path.join(os.getcwd(), folder))] # all images of given digit
    for file in files:
        source = folder+"/"+file
        image = cv2.imread(source, 0)

        f_image = Image.fromarray(image, "L")
        f_image.save(source)

        i = 0
        for kernel in kernels:
            transformed = transform(kernel, f_image) # apply convolution
            
            f = file.split(".")[0] + f"{i}.png"
            transformed.save(f"{folder}/{f}") # save new image

            i += 1

