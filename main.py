from BoardGame import BoardGame
from GameMaster import GameMaster
from Common import Common

import tkinter as tk
from tkinter import ttk

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = tk.Tk()
    size = str(Common.WINDOW_WIDTH) + 'x' + str(Common.WINDOW_HEIGHT)
    #root.geometry('560x560')
    root.geometry(size)
    root.resizable(width=False, height=False)
    root.title('BoardGame')
    app = BoardGame(root)
    app.start()
    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
