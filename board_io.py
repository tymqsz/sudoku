import os
from keras import models
import numpy as np

from image_processing import DigitImage, SudokuImage

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # make tf not print garbage onto terminal
model = models.load_model("resources/models/model.keras")

def print_board(board):
    hor_line = ""

    hor_line += " ---" * 9

    for i in range(9):
        print(hor_line)
        print("| ", end="")
        for j in range(9):
            print(board[i][j], end=" | ")
        print()
    print(hor_line)


def board_from_image(filename):
	SudokuImage(filename) # split sudoku board into tiles

    # for each tile use model to predict correspoding digit
	sudoku = []
	for i in range(81):
		file = f"temp/tiles/tile{i}.jpg"
		digit = DigitImage(file)

		pred = np.argmax(model.predict(digit.data, verbose=0)) # preddict correct nr
		sudoku.append(pred)
            
		os.remove(file)

	sudoku = np.array(sudoku).reshape((9, 9))
	
	return sudoku.tolist()
