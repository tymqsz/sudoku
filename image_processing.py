import numpy as np
import cv2
from scipy import ndimage

class DigitImage:
    def __init__(self, file_path):
        # read and crop
        self.img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        self.img = self.img[4:24, 4:24]

        # create and use mask (binary thresholded digit image)
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
        
        # >30 pixels are white => image considered not empty
        if nr_white >= 30: 
            return False
        return True
        
    def center(self):        
        _, thresh = cv2.threshold(self.img, 80 ,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU) # otsu threshold image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # find contours


        # find biggest contour based on its area+arcLength
        max_val = -1
        biggest_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            arcLen = cv2.arcLength(contour, closed=False)

            if area+arcLen > max_val:
                max_val = area+arcLen
                biggest_contour = contour
        
        # if there is no contour consider image as empty
        if biggest_contour is None:
            self.img = np.zeros((28, 28))
            return
                        
        # extract corners of the biggest contour
        corners = DigitImage.get_corners(biggest_contour).astype(int)

        # get bounds of actual digit inside image
        left = min(corners[:, 1])
        right = max(corners[:, 1])
        up = min(corners[:, 0])
        down = max(corners[:, 0])

        # add safety margin (of 2 pixels)
        left = max(0, left-2)
        right = min(27, right+2)
        up = max(0, up-2)
        down = min(27, down+2)

        # extract part of image containing only digit
        self.img = self.img[left:right, up:down]

        rows = self.img.shape[1]
        cols = self.img.shape[0]

        # add black borders around digit
        left_border = (28-rows) // 2
        right_border  = 28-rows-left_border
        top_border = (28-cols) // 2
        bot_border  = 28-cols-top_border
        self.img = cv2.copyMakeBorder(self.img, top_border, bot_border, left_border,
                                      right_border, cv2.BORDER_CONSTANT, None, (0, 0, 0))


        # shift image based on center of mass
        cy, cx = ndimage.measurements.center_of_mass(self.img)
        rows, cols = self.img.shape
        shiftx = np.round(cols/2.0-cx).astype(int)
        shifty = np.round(rows/2.0-cy).astype(int)
        M = np.float32([[1,0,shiftx],[0,1,shifty]])
        shifted = cv2.warpAffine(self.img, M,(cols,rows))
        
        self.img = np.array(shifted).reshape((28,28))

        _, self.img = cv2.threshold(self.img, 127, 255, cv2.THRESH_TOZERO+cv2.THRESH_OTSU) 

    @staticmethod
    def get_corners(contour):
        # method finding corners of a contour based
        # on differeces and sums of (x, y) coordinates of each point

        min_sum = np.inf
        max_sum = 0
        min_diff = np.inf
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
        # convert to grayscale
        self.gray = cv2.imread(file_path, 0) 

        # make background black, digits white
        self.gray_inv = cv2.bitwise_not(self.gray)

        self.center()

        self.divide_into_tiles()

    def center(self):
        # threshold and find contours
        thresh = cv2.adaptiveThreshold(self.gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3 )
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
        
        # find two biggest contours based on its areas
        biggest_contour = None
        second_biggest_contour = None
        max_val = 0
        second_max_val = 0
        for contour in contours:
            area = cv2.contourArea(contour)

            if area > max_val:
                second_max_val = max_val
                max_val = area
                second_biggest_contour = biggest_contour
                biggest_contour = contour

            elif area > second_max_val:
                second_max_val = area
                second_biggest_contour = contour
        
        corners = SudokuImage.get_corners(biggest_contour)

        # make sure not to detect edges of image as edges of sudoku board
        if [0, 0] in corners or [270, 0] in corners or [0, 270] in corners or [270, 270] in corners:
            corners = SudokuImage.get_corners(second_biggest_contour)
        new_corners = np.array([[0, 0], [270, 0], [0, 270], [270, 270]], dtype=np.float32)

        # warp perspective
        trans_matrix = cv2.getPerspectiveTransform(corners, new_corners)
        transformed = cv2.warpPerspective(self.gray_inv, trans_matrix, (270, 270))
            
        self.img = transformed

    @staticmethod
    def get_corners(contour):
        min_sum = np.inf
        max_sum = 0
        min_diff = np.inf
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
        
                
    # function splitting whole board into 81 tiles and
    # saving them in separate files
    def divide_into_tiles(self):
        M = 30
        N = 30
        imgheight = self.img.shape[1]
        imgwidth = self.img.shape[0]

        image_copy = self.img.copy()

        i = 0
        for y in range(0, imgheight-M+1, M):
            for x in range(0, imgwidth-N+1, N):
                tiles = image_copy[y:y+M, x:x+N]
                cv2.imwrite('temp/tiles/'+'tile'+f'{i}.jpg', tiles)
                i += 1

