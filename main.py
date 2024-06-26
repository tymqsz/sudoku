from gui import App
from board_io import *

os.makedirs("temp/tiles")

main_window = App()
main_window.mainloop()

os.removedirs("temp/tiles")
