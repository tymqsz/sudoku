from tkinter import *
from tech import *
from board_io import *
import random

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.geometry("1200x900")
        self.config(bg="grey78")

        self.crt_nr = None
        self.crt_box = None
        self.tg_nr = [False for i in range(10)]
        self.tg_box = [[False] * 9 for i in range(9)]
        self.fixed = [[False] * 9 for i in range(9)]
        self.box = [[object] * 1000 for i in range(1000)]
        self.nr = [object for i in range(10)]
        self.BOARD = []
        self.result = []
        
        self.fix_mode = True

        self.pixel = PhotoImage()
        self.right = PhotoImage(file="resources/right.png")
        self.left = PhotoImage(file="resources/left.png")
        self.up = PhotoImage(file="resources/up.png")
        self.down = PhotoImage(file="resources/down.png")

        self.cornerNE = PhotoImage(file="resources/cornerNE.png")
        self.cornerNW = PhotoImage(file="resources/cornerNW.png")
        self.cornerSE = PhotoImage(file="resources/cornerSE.png")
        self.cornerSW = PhotoImage(file="resources/cornerSW.png")

        self.oper = Canvas(self, bg="pink", height=500, width=300)
        self.output = Label(master=self.oper, bg="PaleVioletRed", width=220, height=80, image=self.pixel, compound="c", font=("ariel", 20))
        self.new_board_btn = Button(master=self.oper, image=self.pixel, bg="grey78", width=180, height=80, text="new sudoku", compound="c",
                            command=lambda: self.new_board(True), font=("ariel", 24), padx=0, pady=0)
        self.solve_btn = Button(master=self.oper, image=self.pixel, bg="grey78", width=180, height=80, text="solve", compound="c",
                        command=lambda: self.solve(self.BOARD), font=("ariel", 24), padx=0, pady=0)


        self.easy = Button(master=self.oper, image=self.pixel, bg="red4", width=180, height=80, text="easy", compound="c", font=("ariel", 24),
                    padx=0, pady=0, command=lambda: self.gen_b("easy"))
        self.hard = Button(master=self.oper, image=self.pixel, bg="red4", width=180, height=80, text="hard", compound="c", font=("ariel", 24),
                    padx=0, pady=0, command=lambda: self.gen_b("hard"))
        self.vhard = Button(master=self.oper, image=self.pixel, bg="red4", width=180, height=80, text="v.hard", compound="c",
                    font=("ariel", 24), padx=0, pady=0, command=lambda: self.gen_b("vhard"))
		
        self.import_canvas = Canvas(self, bg="pink", height=180, width=300)
        self.from_image_btn = Button(master=self.import_canvas, image=self.pixel, bg="grey78", width=180, height=80, text="load from img", font=("ariel", 20), padx=0, pady=0)
        self.setup()

        self.after(100, self.background)

    def setup(self):
        for i in range(9):
            for j in range(9):
                self.box[i][j] = Button(bg="grey", image=self.pixel, width=80, height=80, command=lambda k=(i, j): self.toggle_box(k),
                                        compound='c', fg='white', font=("ariel", 24), padx=0, pady=0)
                self.box[i][j].grid(row=i, column=j)

        for i in range(9):
            self.box[i][2].config(image=self.right)
        for i in range(9):
            self.box[i][6].config(image=self.left)

        for i in range(9):
            self.box[2][i].config(image=self.down)
        for i in range(9):
            self.box[6][i].config(image=self.up)

        self.box[2][2].config(image=self.cornerNW)
        self.box[2][6].config(image=self.cornerNE)
        self.box[6][2].config(image=self.cornerSW)
        self.box[6][6].config(image=self.cornerSE)

        for i in range(9):
            ob = Label(width=10, height=3, text="", bg="grey78")
            ob.grid(row=10, column=i)

        for i in range(9):
            self.nr[i] = Button(bg="pink", width=3, height=2, text=f"{i + 1}", command=lambda k=i: self.toggle_nr(k),
                        font=("ariel", 24))
            self.nr[i].grid(row=10, column=i, pady=20)

        self.nr[9] = Button(bg="PaleVioletRed", width=5, height=2, text="erase", command=lambda: self.toggle_nr(9),
                    font=("ariel", 20))
        self.nr[9].grid(row=10, column=9, padx=0)

        self.oper.grid(row=0, column=9, rowspan=7, padx=0)
        self.import_canvas.grid(row = 7, column=9, rowspan=2, padx=80)

        self.import_label = Label(master=self.import_canvas, text="Import from .jpg, .png, .txt", font=("ariel", 16), padx=5, pady=5)
        self.import_label.place(x=0, y=0)

        self.import_input = Entry(master=self.import_canvas, background="gray", font=("ariel", 15))
        self.import_input.place(x=20, y=60)

        self.import_btn = Button(master=self.import_canvas, bg="PaleVioletRed", text="import", font=("ariel", 20), command=self.import_sudoku)
        self.import_btn.place(x=90, y=110)

        self.fix_bnt = Button(master=self.import_canvas, bg="red4", text="fix", font=("ariel", 20), command=self.change_fix_mode)
        self.fix_bnt.place(x=220, y=110)
        
        self.solve_btn.place(x=60, y=120)
        self.new_board_btn.place(x=60, y=20)
        self.output.place(x=40, y=350)

        

    def import_sudoku(self):
        folder = "sudoku_images/"    
        filename = self.import_input.get().strip()

        board = board_from_image(folder+filename)

        for y in range(9):
            for x in range(9):
                if board[y][x] == 0:
                    board[y][x] = " "
                if board[y][x] != " ":
                    self.box[y][x].config(text=f"{board[y][x]}", fg="black")
                    self.fixed[y][x] = True
                else:
                    self.box[y][x].config(text=f"", fg="black")
                    self.fixed[y][x] = False
        self.BOARD = [x[:] for x in board]

    def win_popup(self):
        popup = Toplevel(self)
        popup.geometry("300x200")
        popup.config(bg="pink")
        tit = Label(master=popup, text="Sudoku complete!", font=("ariel", 24), width=15, height=1, bg="pink")
        tit.pack(anchor="n")

        kupa1 = Label(master=popup, height=2, bg="pink")
        kupa1.pack()

        new_game_btn = Button(master=popup, text="new game", font=("ariel", 24), width=10, height=1, bg="pink",
                            command=lambda: self.new_game(popup))
        new_game_btn.pack()

        kupa1 = Label(master=popup, height=1, bg="pink")
        kupa1.pack()

        quit_btn = Button(master=popup, text="quit", command=quit, bg="pink", font=("ariel", 16))
        quit_btn.pack()

    
    def change_fix_mode(self):
        self.fix_mode = not self.fix_mode

    def new_game(self, popup):
        popup.destroy()
        self.new_board(True)


    def toggle_nr(self, n):
        if self.tg_nr[n]:
            self.tg_nr[n] = False
            self.crt_nr = None
            self.nr[n].config(bg="pink")
        else:
            self.output["text"] = ''
            self.tg_nr[n] = True
            self.crt_nr = n + 1
            self.nr[n].config(bg="maroon1")
            for i in range(9):
                if i != n:
                    self.tg_nr[i] = False
                    self.nr[i].config(bg="pink")


    def toggle_box(self, s):
        lock = locked(self.BOARD)
        y = s[0]
        x = s[1]
        if self.tg_box[y][x]:
            self.tg_box[y][x] = False
            self.crt_box = None
            self.box[y][x].config(bg="grey")
        else:
            self.output["text"] = ''
            self.tg_box[y][x] = True
            if not lock[y][x] or self.fix_mode:
                self.box[y][x].config(bg="black")
            self.crt_box = (y, x)
            for i in range(9):
                for j in range(9):
                    if not (i == y and j == x):
                        self.box[i][j].config(bg="grey")
                        self.tg_box[i][j] = False


    def gen_b(self, level):
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
                    self.box[y][x].config(text=f"{board[y][x]}", fg="black")
                    self.fixed[y][x] = True
                else:
                    self.box[y][x].config(text=f"", fg="black")
                    self.fixed[y][x] = False

        self.BOARD = [x[:] for x in board]
        self.easy.place_forget()
        self.hard.place_forget()
        self.vhard.place_forget()
        self.new_board_btn.place(x=60, y=20)
        self.solve_btn.place(x=60, y=120)


    def new_board(self, click):
        if click:
            self.new_board_btn.place_forget()
            self.solve_btn.place_forget()
            self.easy.place(x=60, y=20)
            self.hard.place(x=60, y=120)
            self.vhard.place(x=60, y=220)
        else:
            self.gen_b("easy")


    def solve(self, board):
        lock = locked(board)
        result = solve(board, lock)
        for y in range(9):
            for x in range(9):
                val = result[y][x]
                if not lock[y][x]:
                    update(self.BOARD, y + 1, x + 1, val)
                    self.box[y][x].configure(text=f"{val}", fg="white")


    def complete(self):
        if self.BOARD == []:
            return
        N = 0

        for y in range(9):
            for x in range(9):
                if self.BOARD[y][x] != " ":
                    N += 1

        return N == 81


    def background(self):
        if self.crt_box is not None and self.crt_nr is not None:
            y = self.crt_box[0]
            x = self.crt_box[1]
            val = self.crt_nr

            if self.fixed[y][x] and not self.fix_mode:
                print('fixed')
            else:
                if val == 10:
                    update(self.BOARD, y + 1, x + 1, " ")
                    self.box[y][x].configure(text="")
                elif valid_placement(self.BOARD, y + 1, x + 1, val):
                    self.box[y][x].configure(text=f"{val}", fg="white")
                    update(self.BOARD, y + 1, x + 1, val)
                else:
                    self.output["text"] = "invalid placement!"
                    print("invalid placement")
            self.toggle_box((y, x))
            self.toggle_nr(val - 1)

        if self.complete() and self.prev_board != self.BOARD:
            self.win_popup()
        
        self.prev_board = [x[:] for x in self.BOARD]
        self.after(100, self.background)
