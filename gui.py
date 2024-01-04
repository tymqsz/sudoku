from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import time
from tech import *
import random

root = Tk()
root.title("Sudoku")
root.geometry("1200x1000")
root.config(bg="grey78")

crt_nr = None
crt_box = None
tg_nr = [False for i in range(10)]
tg_box = [[False] * 9 for i in range(9)]
fixed = [[False] * 9 for i in range(9)]
box = [[object] * 1000 for i in range(1000)]
nr = [object for i in range(10)]
BOARD = []
result = []

pixel = PhotoImage()
right = PhotoImage(file="right.png")
left = PhotoImage(file="left.png")
up = PhotoImage(file="up.png")
down = PhotoImage(file="down.png")

cornerNE = PhotoImage(file="cornerNE.png")
cornerNW = PhotoImage(file="cornerNW.png")
cornerSE = PhotoImage(file="cornerSE.png")
cornerSW = PhotoImage(file="cornerSW.png")

oper = Canvas(root, bg="pink", height=500, width=300)
output = Label(master=oper, bg="PaleVioletRed", width=220, height=80, image=pixel, compound="c", font=("ariel", 20))
new_board_btn = Button(master=oper, image=pixel, bg="grey78", width=180, height=80, text="new sudoku", compound="c",
                       command=lambda: new_board(True), font=("ariel", 24), padx=0, pady=0)
solve_btn = Button(master=oper, image=pixel, bg="grey78", width=180, height=80, text="solve", compound="c",
                   command=lambda: solverize(BOARD), font=("ariel", 24), padx=0, pady=0)


easy = Button(master=oper, image=pixel, bg="red4", width=180, height=80, text="easy", compound="c", font=("ariel", 24),
              padx=0, pady=0, command=lambda: gen_b("easy"))
hard = Button(master=oper, image=pixel, bg="red4", width=180, height=80, text="hard", compound="c", font=("ariel", 24),
              padx=0, pady=0, command=lambda: gen_b("hard"))
vhard = Button(master=oper, image=pixel, bg="red4", width=180, height=80, text="v.hard", compound="c",
               font=("ariel", 24), padx=0, pady=0, command=lambda: gen_b("vhard"))


def setup():
    for i in range(9):
        for j in range(9):
            box[i][j] = Button(bg="grey", image=pixel, width=80, height=80, command=lambda k=(i, j): toggle_box(k),
                               compound='c', fg='white', font=("ariel", 24), padx=0, pady=0)
            box[i][j].grid(row=i, column=j)

    for i in range(9):
        box[i][2].config(image=right)
    for i in range(9):
        box[i][6].config(image=left)

    for i in range(9):
        box[2][i].config(image=down)
    for i in range(9):
        box[6][i].config(image=up)

    box[2][2].config(image=cornerNW)
    box[2][6].config(image=cornerNE)
    box[6][2].config(image=cornerSW)
    box[6][6].config(image=cornerSE)

    for i in range(9):
        ob = Label(width=10, height=3, text="", bg="grey78")
        ob.grid(row=10, column=i)

    for i in range(9):
        nr[i] = Button(bg="pink", width=3, height=2, text=f"{i + 1}", command=lambda k=i: toggle_nr(k),
                       font=("ariel", 24))
        nr[i].grid(row=11, column=i)

    nr[9] = Button(bg="PaleVioletRed", width=5, height=2, text="erase", command=lambda: toggle_nr(9),
                   font=("ariel", 20))
    nr[9].grid(row=11, column=9, padx=0)

    oper.grid(row=0, column=9, rowspan=10, padx=80)

    solve_btn.place(x=60, y=120)

    new_board_btn.place(x=60, y=20)

    output.place(x=40, y=350)


def solve(board, lock):
    flag = False
    result = []

    def recursive_solve1(board, y, x, lock):
        nonlocal flag, result
        if flag:
            return
        if y > 9 or x > 9:
            result = [s[:] for s in board]
            flag = True
            return

        if lock[y - 1][x - 1]:
            new_x = 0
            new_y = y
            if x == 9:
                new_x = 1
                new_y = y + 1
            else:
                new_x = x + 1
            recursive_solve1(board, new_y, new_x, lock)
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
                recursive_solve1(copy, new_y, new_x, lock)
            update(copy, y, x, " ")
    recursive_solve1(board, 1, 1, lock)
    return result


def win_popup():
    popup = Toplevel(root)
    popup.geometry("300x200")
    popup.config(bg="pink")
    tit = Label(master=popup, text="Sudoku complete!", font=("ariel", 24), width=15, height=1, bg="pink")
    tit.pack(anchor="n")

    kupa1 = Label(master=popup, height=2, bg="pink")
    kupa1.pack()

    new_game_btn = Button(master=popup, text="new game", font=("ariel", 24), width=10, height=1, bg="pink",
                          command=lambda: new_game(popup))
    new_game_btn.pack()

    kupa1 = Label(master=popup, height=1, bg="pink")
    kupa1.pack()

    quit_btn = Button(master=popup, text="quit", command=quit, bg="pink", font=("ariel", 16))
    quit_btn.pack()


def new_game(popup):
    popup.destroy()
    new_board(True)


def toggle_nr(n):
    global crt_nr
    if tg_nr[n]:
        tg_nr[n] = False
        crt_nr = None
        nr[n].config(bg="pink")
    else:
        output["text"] = ''
        tg_nr[n] = True
        crt_nr = n + 1
        nr[n].config(bg="maroon1")
        for i in range(9):
            if i != n:
                tg_nr[i] = False
                nr[i].config(bg="pink")


def toggle_box(s):
    lock = locked(BOARD)
    global crt_box
    y = s[0]
    x = s[1]
    if tg_box[y][x]:
        tg_box[y][x] = False
        crt_box = None
        box[y][x].config(bg="grey")
    else:
        output["text"] = ''
        tg_box[y][x] = True
        if not lock[y][x]:
            box[y][x].config(bg="black")
        crt_box = (y, x)
        for i in range(9):
            for j in range(9):
                if not (i == y and j == x):
                    box[i][j].config(bg="grey")
                    tg_box[i][j] = False


def gen_b(level):
    global BOARD
    root.after(100, background)
    fix = 0

    if level == "easy":
        fix = random.randrange(35, 42)
    elif level == "hard":
        fix = random.randrange(28, 35)
    else:
        fix = random.randrange(22, 28)

    board = generate(fixed=fix)

    for y in range(9):
        for x in range(9):
            if board[y][x] != " ":
                box[y][x].config(text=f"{board[y][x]}", fg="black")
                fixed[y][x] = True
            else:
                box[y][x].config(text=f"", fg="black")
                fixed[y][x] = False

    BOARD = [x[:] for x in board]
    easy.place_forget()
    hard.place_forget()
    vhard.place_forget()
    new_board_btn.place(x=60, y=20)
    solve_btn.place(x=60, y=120)


def new_board(click, **kwargs):
    if click:
        new_board_btn.place_forget()
        solve_btn.place_forget()
        easy.place(x=60, y=20)
        hard.place(x=60, y=120)
        vhard.place(x=60, y=220)
    else:
        gen_b("easy")


def solverize(board, **kwargs):
    lock = locked(board)
    result = solve(board, lock)

    for y in range(9):
        for x in range(9):
            val = result[y][x]
            if not lock[y][x]:
                update(BOARD, y + 1, x + 1, val)
                box[y][x].configure(text=f"{val}", fg="white")


def complete(board):
    N = 0

    for y in range(9):
        for x in range(9):
            if board[y][x] != " ":
                N += 1

    return N == 81


def background():
    global crt_nr, crt_box, fixed, BOARD

    if crt_box is not None and crt_nr is not None:
        y = crt_box[0]
        x = crt_box[1]
        val = crt_nr

        if fixed[y][x]:
            print('fixed')
        else:
            if val == 10:
                update(BOARD, y + 1, x + 1, " ")
                box[y][x].configure(text="")
            elif valid_placement(BOARD, y + 1, x + 1, val):
                box[y][x].configure(text=f"{val}", fg="white")
                update(BOARD, y + 1, x + 1, val)
            else:
                output["text"] = "invalid placement!"
                print("invalid placement")
        toggle_box((y, x))
        toggle_nr(val - 1)

    if complete(BOARD):
        win_popup()
        return

    root.after(100, background)


def main():
    setup()
    root.mainloop()


main()
