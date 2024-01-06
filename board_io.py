import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from image_processing import DigitImage, SudokuImage
from keras import models
import numpy as np

model = models.load_model("models/digitModel.keras")

def print_board(board, **kwargs):
    hor_line = ""
    hor_label = ""
    ver_labels = [chr(65 + i) for i in range(9)]

    if "labels" in kwargs.keys():
        labels = kwargs["labels"]
    else:
        labels = False

    if labels:
        hor_label += "  "
        hor_line += "  "
        for i in range(1, 10):
            hor_label += f"  {i} "
        print(hor_label)

    hor_line += " ---" * 9

    for i in range(9):
        print(hor_line)
        if labels:
            print(ver_labels[i], end=" ")
        print("| ", end="")
        for j in range(9):
            print(board[i][j], end=" | ")
        print()
    print(hor_line)


def board_from_txt(filename):
    with open(filename) as source:
        l = source.readlines()
        shit = []
        for line in l:
            k = line.split("|")
            shit.append(k)
    i = 1
    good = []
    while i <= 17:
        c = shit[i][1:len(shit[i]) - 1][:]
        j = 0
        while j < len(c):
            c[j] = c[j].strip()
            if c[j] == "":
                c[j] = " "
            else:
                c[j] = int(c[j])
            j += 1
        good.append(c)
        i += 2
    return good

def board_from_image(filename):
	image = SudokuImage(filename)

	sudoku = []
	for i in range(81):
		digit = DigitImage(f"tiles/tile{i}.jpg")

		pred = np.argmax(model.predict(digit.data, verbose=0))
		sudoku.append(pred)

	sudoku = np.array(sudoku).reshape((9, 9))
	
	return sudoku.tolist()
