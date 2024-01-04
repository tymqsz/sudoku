import random
import time
import copy

result = []
main_board = [[" " for i in range(9)] for j in range(9)]

N = 0
stop = False


def update(board, y, x, val):
    board[y - 1][x - 1] = val


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


def valid_placement(board, y, x, val):
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
    b = block[y][x]

    for i in range(9):
        for j in range(9):
            if b == block[i][j] and board[i][j] == val and i != y and j != x:
                return False

    for i in range(9):
        if board[y][i] == val and i != x:
            return False
    for i in range(9):
        if board[i][x] == val and i != y:
            return False

    return True


def solution_dict(board):
    result = {}
    possible = [x for x in range(1, 10)]

    for y in range(1, 10):
        crt = []
        for x in range(1, 10):
            for val in possible:
                if board[y - 1][x - 1] == " " and valid_placement(board, y, x, val):
                    crt.append(val)
            result[y, x] = [s for s in crt]
            crt = []

    return result


def import_board(filename):
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


def recursive_solve(board, y, x, lock):
    global result
    if y > 9 or x > 9:
        result = [s[:] for s in board]
        return

    if lock[y - 1][x - 1]:
        new_x = 0
        new_y = y
        if x == 9:
            new_x = 1
            new_y = y + 1
        else:
            new_x = x + 1
        recursive_solve(board, new_y, new_x, lock)
        return
    p = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    copy = [x[:] for x in board]
    for val in p:
        update(copy, y, x, val)
        if valid_placement(board, y, x, val):
            new_x = 0
            new_y = y
            if x == 9:
                new_x = 1
                new_y = y + 1
            else:
                new_x = x + 1
            recursive_solve(copy, new_y, new_x, lock)
        update(copy, y, x, " ")


def solve111(board, **kwargs):
    print_board(board)
    start = time.time()
    p = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    previous = []

    if "live" in kwargs.keys():
        live = kwargs["live"]
    else:
        live = False
    if "stats" in kwargs.keys():
        stats = kwargs["stats"]
    else:
        stats = False

    possible = solution_dict(board)
    for y in range(1, 10):
        for x in range(1, 10):
            if len(possible[y, x]) == 1:
                val = possible[y, x][0]
                update(board, y, x, val)

    lock = locked(board)

    x, y = 1, 1
    direction = "front"
    while y <= 9 and x <= 9:
        if live:
            cell = (y - 1) * 9 + x
            print(f"cell: {cell}, no of iter: {len(previous)}")
        if lock[y - 1][x - 1] == 1:
            if direction == "front":
                if x == 9:
                    x = 1
                    y += 1
                else:
                    x += 1
            else:
                if x == 1:
                    x = 9
                    y -= 1
                else:
                    x -= 1
            continue

        none_valid = True
        last = [x[:] for x in board]

        for val in p:
            update(last, y, x, val)
            simply = simplified(last)
            is_valid = valid_placement(board, y, x, val)

            if simply not in previous:
                if is_valid:
                    none_valid = False
                else:
                    previous.append(simply)

        if none_valid:
            update(board, y, x, " ")
            direction = "back"
            if x == 1:
                x = 9
                y -= 1
            else:
                x -= 1
        else:
            tried = False
            pos = [v for v in possible[y, x]]
            while not tried:
                val = pos[0]
                update(last, y, x, val)
                simply = simplified(last)

                if simply not in previous and valid_placement(board, y, x, val):
                    tried = True
                    previous.append(simply)
                    update(board, y, x, val)

                    direction = "front"
                    if x == 9:
                        x = 1
                        y += 1
                    else:
                        x += 1
                else:
                    pos.pop(pos.index(val))

    end = time.time()
    solve_time = round(end - start, 3)
    iterations = len(previous)

    if stats:
        print(f"solved in {solve_time}s ({iterations} iterations)")


def simplified(board):
    result = []

    for row in board:
        for i in row:
            result.append(i)

    return result


def check_board(board):
    all_good = True
    y = 1
    x = 1
    for row in board:
        x = 1
        for i in row:
            val = int(i)
            if not valid_placement(board, y, x, val):
                print(f"invalid postion {y, x} ({val})")
                all_good = False
            x += 1
        y += 1

    if all_good:
        print("valid board")


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

        update(board, hole[0], hole[1], " ")

        cnt += 1


def locked(board):
    result = []

    for row in board:
        r = []
        for i in row:
            if i == " ":
                r.append(0)
            else:
                r.append(1)
        result.append(r)

    return result


# noinspection PyTypeChecker
def main():
    global result
    global N
    row = {chr(97 + i): (i + 1) for i in range(9)}

    game_over = True

    main_board = generate_board(fixed=30)
    result = []
    lock = locked(main_board)
    recursive_solve(main_board, 1, 1, lock)
    print_board(result)

    while not game_over:
        print_board(main_board, labels=True)
        play = input("play: ")
        play = play.strip().lower()

        if play == "stop":
            game_over = True
            continue

        play = play.split()
        if len(play) < 2:
            print("incorrect input")
            continue
        elif len(play) == 2:
            if not play[1].isdigit():
                print("incorrect input")
                continue
            play[1] = int(play[1])
            if play[0][0] not in row.keys() or int(play[0][1]) < 1 or int(play[0][1]) > 9 or play[1] < 1 or play[1] > 9:
                print("incorrect input")
                continue
            y = row[play[0][0]]
            x = int(play[0][1])
            val = play[1]
        else:
            if not play[2].isdigit():
                print("incorrect input")
                continue
            play[2] = int(play[2])
            if play[0] not in row.keys() or int(play[1]) < 1 or int(play[1]) > 9 or play[2] < 1 or play[2] > 9:
                print("incorrect input")
                continue
            y = row[play[0]]
            x = int(play[1])
            val = play[2]

        if not valid_placement(main_board, y, x, val):
            print("invalid placement")
            continue
        update(main_board, y, x, val)


def generate(fixed):
    new_board = [[" " for i in range(9)] for j in range(9)]
    p = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    previous = []

    x, y = 1, 1
    while y <= 9 and x <= 9:
        none_valid = True
        last = [s[:] for s in new_board]

        for val in p:
            last[y - 1][x - 1] = val
            simply = simplified(last)
            is_valid = valid_placement(new_board, y, x, val)

            if simply not in previous:
                if is_valid:
                    none_valid = False
                else:
                    previous.append(simply)

        if none_valid:
            new_board[y - 1][x - 1] = " "
            if x == 1:
                x = 9
                y -= 1
            else:
                x -= 1
        else:
            tried = False
            possible = p[:]
            while not tried:
                val = random.choice(possible)
                last[y - 1][x - 1] = val
                simply = simplified(last)

                if simply not in previous and valid_placement(new_board, y, x, val):
                    tried = True
                    previous.append(simply)
                    new_board[y - 1][x - 1] = val

                    if x == 9:
                        x = 1
                        y += 1
                    else:
                        x += 1
                else:
                    possible.pop(possible.index(val))

    possible = []
    n = 81 - fixed
    for y in range(1, 10):
        for x in range(1, 10):
            crt = (y, x)
            possible.append(crt)

    cnt = 0
    while cnt < n:
        hole = random.choice(possible)
        possible.pop(possible.index(hole))

        new_board[hole[0] - 1][hole[1] - 1] = " "
        cnt += 1

    return new_board


