from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

from Common import Common
from Unit import UnitKind
from Player import PlayerKind
from GameMaster import GameResult
from GameDisplay import GameDisplay

class AppDisplay:
    def __init__(self, root):

        self.root = root

        # 対戦画面
        self.app_frame = tk.Frame(self.root, width=Common.WINDOW_WIDTH, height=Common.WINDOW_HEIGHT, bg='White')
        self.app_frame.place(x=0, y=0)

    def create_game_display(self):

        self.game_display = GameDisplay(self.app_frame)

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




