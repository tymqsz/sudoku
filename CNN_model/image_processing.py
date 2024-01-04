from PIL import Image
import numpy as np
import cv2
import math
from scipy import ndimage

class DigitImage:
    def __init__(self, file_path):
        self.img = cv2.imread(file_path, 0)
        self.center()

    def center(self):
        digit = self.img

        non_zero_rows = np.where(np.sum(digit, axis=1) > 0)[0]
        non_zero_cols = np.where(np.sum(digit, axis=0) > 0)[0]

        digit = digit[min(non_zero_rows):max(non_zero_rows) + 1, min(non_zero_cols):max(non_zero_cols) + 1]


        rows, cols = digit.shape
        if rows > cols:
            factor = 20.0/rows
            rows = 20
            cols = int(round(cols*factor))
            digit = cv2.resize(digit, (cols, rows))
        else:
            factor = 20.0/cols
            cols = 20
            rows = int(round(rows*factor))
            digit = cv2.resize(digit, (cols, rows))

        colsPadding = (int(math.ceil((28-cols)/2.0)),int(math.floor((28-cols)/2.0)))
        rowsPadding = (int(math.ceil((28-rows)/2.0)),int(math.floor((28-rows)/2.0)))
        digit = np.lib.pad(digit,(rowsPadding,colsPadding),'constant')
        cy, cx = ndimage.measurements.center_of_mass(digit)

        
        rows, cols = digit.shape
        shiftx = np.round(cols/2.0-cx).astype(int)
        shifty = np.round(rows/2.0-cy).astype(int)
        M = np.float32([[1,0,shiftx],[0,1,shifty]])
        shifted = cv2.warpAffine(digit, M,(cols,rows))
        
        self.img = shifted
        self.raw = np.array(self.img).reshape(1, 28, 28, -1)
            