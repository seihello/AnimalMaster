from App import App
from Common import Common

import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    size = str(Common.WINDOW_WIDTH) + 'x' + str(Common.WINDOW_HEIGHT)
    root.geometry(size)
    root.resizable(width=False, height=False)
    root.title('BoardGame')
    app = App(root)
    app.start()
    root.mainloop()