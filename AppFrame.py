from PIL import Image, ImageTk
from tkinter import messagebox, Frame

from Common import Common
from GameMaster import GameResult

class AppFrame(Frame):
    def __init__(self, root):

        super().__init__(root, width=Common.WINDOW_WIDTH, height=Common.WINDOW_HEIGHT, bg='red')

        self.root = root

    def show_result(self, game_result, lower_player, upper_player):
        if game_result == GameResult.LOWER_WIN:
            message = lower_player.__class__.__name__ + "の勝利です"
        elif game_result == GameResult.UPPER_WIN:
            message = upper_player.__class__.__name__ + "の勝利です"
        elif game_result == GameResult.DRAW:
            message = "引き分けです"
        self.root.after(200, lambda: messagebox.showinfo('ゲーム終了', message))

    def get_image(self, file_name):
        image = Image.open(file_name)
        return ImageTk.PhotoImage(image=image)




