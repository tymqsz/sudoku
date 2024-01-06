from PIL import Image
import numpy as np
import cv2
import math
from scipy import ndimage
import matplotlib.pyplot as plt

class DigitImage:
    def __init__(self, file_path):
        self.path = file_path
        self.img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        self.img = self.img[4:24, 4:24]

        to_mask = self.img.copy()
        self.mask = cv2.adaptiveThreshold(to_mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -10)
        self.img = cv2.bitwise_and(self.img, self.mask)

        if self.is_empty():
            self.img = np.zeros((28, 28), dtype=np.float32)
        else:
            self.center()
        
        cv2.imwrite(file_path, self.img)
        
        self.data = self.img.reshape((1, 28, 28, -1))
            
    def is_empty(self):
        vals = self.mask.flatten()

        nr_white = 0
        for val in vals:
            if val == 255:
                nr_white += 1
        
        if nr_white >= 30:
            return False
        return True
        
    def center(self):        
        digit = self.img

        ret, thresh = cv2.threshold(self.img, 80 ,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

        max_val = -1
        win = None
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            arcLen = cv2.arcLength(contour, closed=False)

            if area+arcLen > max_val:
                max_val = area+arcLen
                win = contour
        if win is None:
            self.img = np.zeros((28, 28))
            return
                        
        
        corners = DigitImage.get_corners(win).astype(int)
        left, right, up, down = 28, 0, 28, 0
        for x in corners[:,1]:
            if x < left:
                left = x
            if x > right:
                right = x
        
        for y in corners[:,0]:
            if y < up:
                up = y
            if y > down:
                down = y
        
        PIXEL_MARGIN = 2

        left -= PIXEL_MARGIN
        right += PIXEL_MARGIN
        up -= PIXEL_MARGIN
        down += PIXEL_MARGIN
        
        left = max(left, 0)
        up = max(up, 0)
        right = min(right, 27)
        down = min(down, 27)

        self.img = self.img[left:right, up:down]

        rows = self.img.shape[1]
        cols = self.img.shape[0]

        left = (28-rows) // 2
        right = 28-rows-left
        top = (28-cols) // 2
        bot = 28-cols-top

        self.img = cv2.copyMakeBorder(self.img, top, bot, left, right, cv2.BORDER_CONSTANT, None, (0, 0, 0))

        cy, cx = ndimage.measurements.center_of_mass(self.img)
        rows, cols = self.img.shape
        shiftx = np.round(cols/2.0-cx).astype(int)
        shifty = np.round(rows/2.0-cy).astype(int)
        M = np.float32([[1,0,shiftx],[0,1,shifty]])
        shifted = cv2.warpAffine(self.img, M,(cols,rows))
        
        self.img = np.array(shifted).reshape((28,28))

        ret, self.img = cv2.threshold(self.img, 127, 255, cv2.THRESH_TOZERO+cv2.THRESH_OTSU) 

    @staticmethod
    def get_corners(contour):
        min_sum = 10000000
        max_sum = 0
        min_diff = 10000000
        max_diff = 0

        tl, tr, bl, br = [0, 0], [0, 0], [0, 0], [0, 0]

        for point in contour:
            point = point[0]
            sum = point[0] + point[1]
            diff = point[0] - point[1]
            if sum < min_sum:
                min_sum = sum
                tl = point
            if sum > max_sum:
                max_sum = sum
                br = point
            if diff < min_diff:
                min_diff = diff
                tr = point
            if diff > max_diff:
                max_diff = diff
                bl = point
        
        return np.array([tl, tr, bl, br], dtype=np.float32)
            

class SudokuImage:
    def __init__(self, file_path):
        self.gray = cv2.imread(file_path, 0)
        self.rgb = cv2.imread(file_path)

        self.gray_inv = cv2.bitwise_not(self.gray)

        self.center()
        self.cut()

    def center(self):
        thresh = cv2.adaptiveThreshold(self.gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3 )
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
        
        win = None
        win2 = None
        maxi = 0
        maxi2 = 0
        for con in contours:
            area = cv2.contourArea(con)

            if area > maxi:
                maxi2 = maxi
                maxi = area
                win2 = win
                win = con
            elif area > maxi2:
                maxi2 = area
                win2 = con
        
        cp = self.rgb.copy()
        cv2.drawContours(cp, win, -1, (255, 255, 255), 3)
        plt.figure()
        plt.imshow(cp)  
        
        corners = SudokuImage.get_corners(win)
        if [0, 0] in corners or [270, 0] in corners or [0, 270] in corners or [270, 270] in corners:
            corners = SudokuImage.get_corners(win2)
        new_corners = np.array([[0, 0], [270, 0], [0, 270], [270, 270]], dtype=np.float32)

        trans_mat = cv2.getPerspectiveTransform(corners, new_corners)
        transformed = cv2.warpPerspective(self.gray_inv, trans_mat, (270, 270))
            
        self.img = transformed


    @staticmethod
    def get_corners(contour):
        min_sum = 10000000
        max_sum = 0
        min_diff = 10000000
        max_diff = 0

        tl, tr, bl, br = [0, 0], [0, 0], [0, 0], [0, 0]

        for point in contour:
            point = point[0]
            sum = point[0] + point[1]
            diff = point[1] - point[0]

            if sum < min_sum:
                min_sum = sum
                tl = point
            if sum > max_sum:
                max_sum = sum
                br = point
            if diff < min_diff:
                min_diff = diff
                tr = point
            if diff > max_diff:
                max_diff = diff
                bl = point
        
        return np.array([tl, tr, bl, br], dtype=np.float32)
        
                

    def cut(self):
        M = 30
        N = 30
        imgheight = self.img.shape[1]
        imgwidth = self.img.shape[0]

        image_copy = self.img.copy()

        i = 0
        for y in range(0, imgheight, M):
            for x in range(0, imgwidth, N):
                if (imgheight - y) < M or (imgwidth - x) < N:
                    break
                    
                tiles = image_copy[y:y+M, x:x+N]
                cv2.imwrite('tiles/'+'tile'+f'{i}.jpg', tiles)
                i += 1

