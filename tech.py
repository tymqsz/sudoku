import random


def generate_board(fixed):
    new_board = [[" " for _ in range(9)] for _  in range(9)]
    possible_nrs = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    failed_boards = [] # array used to store info about previously tried board
                       # used not to generate the same board twice

    # TODO: move x, y by -1
    x, y = 1, 1
    while y <= 9 and x <= 9:
        none_valid = True
        previous = [row[:] for row in new_board]

        # try all possible numbers
        for nr in possible_nrs:
            previous[y - 1][x - 1] = nr
            simplified_board = simplify(previous)

            if simplified_board not in failed_boards:
                if valid_placement(new_board, y, x, nr):
                    none_valid = False
                else:
                    failed_boards.append(simplified_board)

        # if no possible number is valid go back one tile
        if none_valid:
            new_board[y - 1][x - 1] = " "
            if x == 1:
                x = 9
                y -= 1
            else:
                x -= 1
        else: # otherwise try random valid nr and go forward
            tried = False
            possible = possible_nrs[:]
            
            # try all nrs that are valid and that dont produce previously created board
            while not tried:
                nr = random.choice(possible)
                previous[y - 1][x - 1] = nr
                simplified_board = simplify(previous)

                if simplified_board not in failed_boards and valid_placement(new_board, y, x, nr):
                    tried = True
                    failed_boards.append(simplified_board)
                    new_board[y - 1][x - 1] = nr

                    if x == 9:
                        x = 1
                        y += 1
                    else:
                        x += 1
                else:
                    possible.pop(possible.index(nr))
    
    # add all tiles to possible holes
    possible_holes = []
    n = 81 - fixed
    for y in range(1, 10):
        for x in range(1, 10):
            crt = (y, x)
            possible_holes.append(crt)
    
    # make desired nr of holes
    cnt = 0
    while cnt < n:
        hole = random.choice(possible_holes) 
        possible_holes.pop(possible_holes.index(hole)) # remove tile from possible hole

        new_board[hole[0] - 1][hole[1] - 1] = " " # make hole
        cnt += 1

    return new_board


def solve(board, lock):
    solved = False # flag used to stop all recursive calls
    result = []

    # function solving sudoku by recursion based on dfs
    def recursive_solve(board, y, x, locked_tiles):
        nonlocal solved, result
        if solved:
            return
        
        if y > 9 or x > 9:
            result = [s[:] for s in board]
            solved = True
            return

        # if tile locked (solved by default) - skip 
        if locked_tiles[y - 1][x - 1]:
            next_x = 0
            next_y = y

            # if x == 9 go to the next row
            if x == 9: 
                next_x = 1
                next_y = y + 1
            else:
                next_x = x + 1
            
            recursive_solve(board, next_y, next_x, locked_tiles)
            return
        
        possible_nrs = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        board_copy = [row[:] for row in board]

        for nr in possible_nrs:
            update_board(board_copy, y, x, nr)
            if valid_placement(board, y, x, nr):
                next_x = 0
                next_y = y

                # if x == 9 go to the next row
                if x == 9:
                    next_x = 1
                    next_y = y + 1
                else:
                    next_x = x + 1

                recursive_solve(board_copy, next_y, next_x, locked_tiles)
            update_board(board_copy, y, x, " ")

    recursive_solve(board, 1, 1, lock)

    return result

# function used for easier indexing (starting from 1)
def update_board(board, y, x, val):
    board[y - 1][x - 1] = val


def valid_placement(board, y, x, nr):
    # array used for easier checking if all numbers
    # are different in 3x3 sudoku blocks
    block = [[1, 1, 1, 2, 2, 2, 3, 3, 3], 
             [1, 1, 1, 2, 2, 2, 3, 3, 3],
             [1, 1, 1, 2, 2, 2, 3, 3, 3],
             [4, 4, 4, 5, 5, 5, 6, 6, 6],
             [4, 4, 4, 5, 5, 5, 6, 6, 6],
             [4, 4, 4, 5, 5, 5, 6, 6, 6],
             [7, 7, 7, 8, 8, 8, 9, 9, 9],
             [7, 7, 7, 8, 8, 8, 9, 9, 9],
             [7, 7, 7, 8, 8, 8, 9, 9, 9]]


    y -= 1
    x -= 1
    crt_block = block[y][x]

    # check blocks
    for i in range(9):
        for j in range(9):
            if crt_block == block[i][j] and board[i][j] == nr and i != y and j != x:
                return False

    # check rows
    for i in range(9):
        if board[y][i] == nr and i != x:
            return False
    # check columns
    for i in range(9):
        if board[i][x] == nr and i != y:
            return False

    return True

# function flattening array to 1d
def simplify(board):
    result = []

    for row in board:
        for i in row:
            result.append(i)

    return result

# function checking if sudoku is valid
def valid_board(board):
    y = 1
    x = 1
    for row in board:
        x = 1
        for i in row:
            if i == ' ' or i == 0:
                x +=1
                continue
            val = int(i)
            if not valid_placement(board, y, x, val):
                return False
            x += 1
        y += 1

    return True

# function allowing to make additional holes (empty tiles) in sudoku
def make_holes(board, n):
    possible = []

    for y in range(1, 10):
        for x in range(1, 10):
            crt = (y, x)
            possible.append(crt)

    cnt = 0
    while cnt < n:
        hole = random.choice(possible)
        possible.pop(possible.index(hole))

        update_board(board, hole[0], hole[1], " ")

        cnt += 1


# function returning nrs of tiles solved by default
def get_locked_tiles(board):
    locked_tiles = []

    for row in board:
        r = []
        for i in row:
            if i == " ":
                r.append(0)
            else:
                r.append(1)
        locked_tiles.append(r)

    return locked_tiles
