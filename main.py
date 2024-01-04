from gui import App
from board_io import *
import cv2 
import matplotlib.pyplot as plt


file_path = "resources/sudoku.png"

board = board_from_image(file_path)

print(board)
