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

        # structures containing info abouut currently selected number and tile
        self.selected_nr = None
        self.selected_tile = None
        self.nr_pressed = [False for _ in range(10)]
        self.tile_pressed = [[False for _ in range (9)] for _ in range(9)]
        self.tile_fixed = [[False for _ in range(9)] for _ in range(9)]
        self.tile_btn = [[object for _ in range(9)] for _ in range(9)]
        self.nr_btn = [object for _ in range(9)]
        
        self.BOARD = []
        self.result = []
        
        self.fix_mode = False
        self.solvable = False

        # images used for displaying board
        self.pixel = PhotoImage()
        self.right = PhotoImage(file="resources/gui/right.png")
        self.left = PhotoImage(file="resources/gui/left.png")
        self.up = PhotoImage(file="resources/gui/up.png")
        self.down = PhotoImage(file="resources/gui/down.png")
        self.cornerNE = PhotoImage(file="resources/gui/cornerNE.png")
        self.cornerNW = PhotoImage(file="resources/gui/cornerNW.png")
        self.cornerSE = PhotoImage(file="resources/gui/cornerSE.png")
        self.cornerSW = PhotoImage(file="resources/gui/cornerSW.png")

        # canvas used for controling game state
        self.operation_canvas = Canvas(self, bg="pink", height=500, width=300)

        self.output_label = Label(master=self.operation_canvas, bg="PaleVioletRed", 
                                  width=220, height=80, image=self.pixel, 
                                  compound="c", font=("ariel", 20))

        self.new_board_btn = Button(master=self.operation_canvas, image=self.pixel, bg="grey78", 
                                    width=180, height=80, text="new sudoku", compound="c", 
                                    font=("ariel", 24), padx=0, pady=0,
                                    command=lambda: self.load_new_board_canvas())

        self.solve_btn = Button(master=self.operation_canvas, image=self.pixel, bg="grey78", 
                                width=180, height=80, text="solve", compound="c", 
                                font=("ariel", 24), padx=0, pady=0,
                                command=self.load_solved_board)

        self.easy = Button(master=self.operation_canvas, image=self.pixel, bg="red4", 
                           width=180, height=80, text="easy", compound="c",
                           font=("ariel", 24), padx=0, pady=0, 
                           command=lambda: self.new_board("easy"))

        self.hard = Button(master=self.operation_canvas, image=self.pixel, bg="red4", 
                           width=180, height=80, text="hard", compound="c",
                           font=("ariel", 24), padx=0, pady=0, 
                           command=lambda: self.new_board("hard"))

        self.vhard = Button(master=self.operation_canvas, image=self.pixel, bg="red4", 
                           width=180, height=80, text="vhard", compound="c",
                           font=("ariel", 24), padx=0, pady=0, 
                           command=lambda: self.new_board("vhard"))

        
        # canvas used for mporing boards
        self.import_canvas = Canvas(self, bg="pink", height=180, width=300)

        self.setup()

        self.after(100, self.background)

    def setup(self):
        # create buttons used for tile selection
        for i in range(9):
            for j in range(9):
                self.tile_btn[i][j] = Button(bg="grey", image=self.pixel, width=80, height=80, compound='c',
                                             fg='white', font=("ariel", 24), padx=0, pady=0,
                                             command=lambda k=(i, j): self.toggle_box(k))
                self.tile_btn[i][j].grid(row=i, column=j)

        # set proper images for each button (vertical/horizontal lines)
        for i in range(9):
            self.tile_btn[i][2].config(image=self.right)
            self.tile_btn[i][6].config(image=self.left)
            self.tile_btn[2][i].config(image=self.down)
            self.tile_btn[6][i].config(image=self.up) 
        # (corner lines)
        self.tile_btn[2][2].config(image=self.cornerNW)
        self.tile_btn[2][6].config(image=self.cornerNE)
        self.tile_btn[6][2].config(image=self.cornerSW)
        self.tile_btn[6][6].config(image=self.cornerSE)
        
        #for i in range(9):
        #    ob = Label(width=10, height=3, text="", bg="grey78")
        #    ob.grid(row=10, column=i)

        for i in range(9):
            self.nr_btn[i] = Button(bg="pink", width=3, height=2,
                                    text=f"{i + 1}", font=("ariel", 24),
                                    command=lambda k=i: self.toggle_nr(k))
            self.nr_btn[i].grid(row=10, column=i, pady=20)

        self.erase_btn = Button(bg="PaleVioletRed", width=5, height=2,
                                text="erase", font=("ariel", 20),
                                command=lambda: self.toggle_nr(9))
        self.erase_btn.grid(row=10, column=9, padx=0)


        self.operation_canvas.grid(row=0, column=9, rowspan=7, padx=0)
        self.import_canvas.grid(row = 7, column=9, rowspan=2, padx=80)

        self.import_label = Label(master=self.import_canvas, text="Import from .jpg, .png, .txt",
                                   font=("ariel", 16), padx=5, pady=5)
        self.import_label.place(x=0, y=0)

        self.import_input = Entry(master=self.import_canvas, background="gray", font=("ariel", 15))
        self.import_input.place(x=20, y=60)

        self.import_btn = Button(master=self.import_canvas, bg="PaleVioletRed", text="import",
                                 font=("ariel", 20), command=self.import_sudoku)
        self.import_btn.place(x=90, y=110)

        self.fix_bnt = Button(master=self.import_canvas, bg="red4", text="fix",
                              font=("ariel", 20), command=self.change_fix_mode)
        self.fix_bnt.place(x=220, y=110)
        
        self.solve_btn.place(x=60, y=120)
        self.new_board_btn.place(x=60, y=20)
        self.output_label.place(x=40, y=350)

        
    def import_sudoku(self):
        folder = "sudoku_images/"    
        filename = self.import_input.get().strip()

        # import sudoku from image
        board = board_from_image(folder+filename)


        # load imported sudoku to board
        for y in range(9):
            for x in range(9):
                if board[y][x] == 0:
                    board[y][x] = " "
                if board[y][x] != " ":
                    self.tile_btn[y][x].config(text=f"{board[y][x]}", fg="black")
                    self.tile_fixed[y][x] = True
                else:
                    self.tile_btn[y][x].config(text=f"", fg="black")
                    self.tile_fixed[y][x] = False
        self.BOARD = [x[:] for x in board]

    def win_popup(self):
        popup = Toplevel(self)
        popup.geometry("300x200")
        popup.config(bg="pink")
        title_label = Label(master=popup, text="Sudoku complete!",
                            font=("ariel", 24), width=15, height=1, bg="pink")
        title_label.pack(anchor="n")

        # create helper label to make packing easier
        helper = Label(master=popup, height=2, bg="pink")
        helper.pack()

        new_game_btn = Button(master=popup, text="new game", font=("ariel", 24),
                              width=10, height=1, bg="pink",
                              command=lambda: self.new_game(popup))
        new_game_btn.pack()

        # create helper label to make packing easier
        helper = Label(master=popup, height=1, bg="pink")
        helper.pack()

        quit_btn = Button(master=popup, text="quit", command=quit, bg="pink", font=("ariel", 16))
        quit_btn.pack()

    def change_fix_mode(self):
        self.fix_mode = not self.fix_mode

    def new_game(self, popup):
        popup.destroy()
        self.new_board(True)

    def toggle_nr(self, n):
        # if nr_btn already pressed switch it off
        if self.nr_pressed[n]:
            self.nr_pressed[n] = False
            self.selected_nr = None
            self.nr_btn[n].config(bg="pink")
        else: # otherwise turn it on and switch off other btns
            self.output_label["text"] = ''
            self.nr_pressed[n] = True
            self.selected_nr = n + 1
            self.nr_btn[n].config(bg="maroon1")

            for i in range(9):
                if i != n:
                    self.nr_pressed[i] = False
                    self.nr_btn[i].config(bg="pink")


    def toggle_box(self, box):
        locked_tiles = get_locked_tiles(self.BOARD)
        y = box[0]
        x = box[1]

        # if tile_btn already pressed switch it off
        if self.tile_pressed[y][x]:
            self.tile_pressed[y][x] = False
            self.selected_tile = None
            self.tile_btn[y][x].config(bg="grey")
        else: # otherwise turn it on and switch off other btns
            self.output_label["text"] = ''
            self.tile_pressed[y][x] = True

            if not locked_tiles[y][x] or self.fix_mode:
                self.tile_btn[y][x].config(bg="black")
            self.selected_tile = (y, x)

            for i in range(9):
                for j in range(9):
                    if not (i == y and j == x): # switch off all except selected one
                        self.tile_btn[i][j].config(bg="grey")
                        self.tile_pressed[i][j] = False


    def new_board(self, level):
        if level == "easy":
            fixed_tiles_cnt = random.randrange(35, 42)
        elif level == "hard":
            fixed_tiles_cnt = random.randrange(28, 35)
        else:
            fixed_tiles_cnt = random.randrange(22, 28)

        # generate board with nr of complete tiles = fixed_tiles_cnt
        board = generate_board(fixed=fixed_tiles_cnt)

        # load the board
        for y in range(9):
            for x in range(9):
                if board[y][x] != " ":
                    self.tile_btn[y][x].config(text=f"{board[y][x]}", fg="black")
                    self.tile_fixed[y][x] = True
                else:
                    self.tile_btn[y][x].config(text=f"", fg="black")
                    self.tile_fixed[y][x] = False

        self.BOARD = [x[:] for x in board]

        # reload buttons
        self.easy.place_forget()
        self.hard.place_forget()
        self.vhard.place_forget()
        self.new_board_btn.place(x=60, y=20)
        self.solve_btn.place(x=60, y=120)


    def load_new_board_canvas(self):
        self.new_board_btn.place_forget()
        self.solve_btn.place_forget()
        self.easy.place(x=60, y=20)
        self.hard.place(x=60, y=120)
        self.vhard.place(x=60, y=220)


    def load_solved_board(self):
        locked_tiles = get_locked_tiles(self.BOARD)
        solved_board = solve(self.BOARD, locked_tiles)

        for y in range(9):
            for x in range(9):
                val = solved_board[y][x]
                if not locked_tiles[y][x]:
                    update_board(self.BOARD, y + 1, x + 1, val)
                    self.tile_btn[y][x].configure(text=f"{val}", fg="white")

    def board_complete(self):
        if self.BOARD == []:
            return
        
        N = 0
        for y in range(9):
            for x in range(9):
                if self.BOARD[y][x] != " ":
                    N += 1

        return N == 81 # if all tiles filled return True


    def background(self):
        if self.BOARD != []:
            if valid_board(self.BOARD):
                self.output_label["text"] = "valid board"
            else:
                self.output_label["text"] = "invalid board"

        if self.selected_tile is not None and self.selected_nr is not None:
            tile_y = self.selected_tile[0]
            tile_x = self.selected_tile[1]
            selected_nr = self.selected_nr

            if not (self.tile_fixed[tile_y][tile_x] and not self.fix_mode):
                # check if erase btn selected
                if selected_nr == 10: 
                    update_board(self.BOARD, tile_y + 1, tile_x + 1, " ")
                    self.tile_btn[tile_y][tile_x].configure(text="")
                # if valid placement - update board
                elif valid_placement(self.BOARD, tile_y + 1, tile_x + 1, selected_nr):
                    self.tile_btn[tile_y][tile_x].configure(text=f"{selected_nr}", fg="white")
                    update_board(self.BOARD, tile_y + 1, tile_x + 1, selected_nr)
                else:
                    self.output_label["text"] = "invalid placement!"
            self.toggle_box((tile_y, tile_x))
            self.toggle_nr(selected_nr - 1)

        # check if complete and make sure not only one popup is shown
        if self.board_complete() and self.prev_board != self.BOARD:
            self.win_popup()
        
        self.prev_board = [x[:] for x in self.BOARD]

        # run recursively
        self.after(100, self.background)