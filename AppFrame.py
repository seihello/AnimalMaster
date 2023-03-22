from tkinter import Frame, messagebox
from PIL import Image, ImageTk

from Common import Common
from GameManager import GameResult

class AppFrame(Frame):
    def __init__(self, root):

        super().__init__(root, width=Common.WINDOW_WIDTH, height=Common.WINDOW_HEIGHT, bg='red')

        self.root = root

    def show_result(self, game_result, lower_player_name, upper_player_name):
        if game_result == GameResult.LOWER_WIN:
            message = lower_player_name + "の勝利です"
        elif game_result == GameResult.UPPER_WIN:
            message = upper_player_name + "の勝利です"
        elif game_result == GameResult.DRAW:
            message = "引き分けです"
        self.root.after(100, lambda: messagebox.showinfo('ゲーム終了', message))

    def get_image(self, file_name):
        image = Image.open(file_name)
        return ImageTk.PhotoImage(image=image)




