from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

from Common import Common
from Unit import UnitKind
from Player import PlayerKind

from tkinter import Canvas

class StatusCanvas(Canvas):
    def __init__(self, app_frame):

        super().__init__(app_frame, width=Common.STATUS_CANVAS_WIDTH, height=Common.STATUS_CANVAS_HEIGHT,
                         highlightthickness=0, background='Blue')

        self.app_frame = app_frame

        self.status_bg_image = self.get_image("component/status_bg.png")
        self.create_image(0, 0, image=self.status_bg_image, anchor='nw')

        self.create_text(Common.STATUS_CANVAS_WIDTH // 4,
                         Common.STATUS_CANVAS_HEIGHT // 3 * 2 + 5,
                         text='3',
                         fill='White',
                         font=("MSゴシック", "38", "bold"),
                         tag='lower_win_count')

        self.create_text(Common.STATUS_CANVAS_WIDTH // 4 * 3,
                         Common.STATUS_CANVAS_HEIGHT // 3 * 2 + 5,
                         text='3',
                         fill='White',
                         font=("MSゴシック", "38", "bold"),
                         tag='upper_win_count')

    def draw_player_name(self, lower_player_name, upper_player_name):

        self.create_text(Common.STATUS_CANVAS_WIDTH // 4,
                         20,
                         text=lower_player_name,
                         fill='White',
                         font=("MSゴシック", "24", "bold"))

        self.create_text(Common.STATUS_CANVAS_WIDTH // 4 * 3,
                         20,
                         text=upper_player_name,
                         fill='White',
                         font=("MSゴシック", "24", "bold"))


    def update_win_count(self, lower_win_count, upper_win_count, draw_count):

        self.itemconfig('lower_win_count', text=str(lower_win_count))
        self.itemconfig('upper_win_count', text=str(upper_win_count))

    def get_image(self, file_name):
        image = Image.open("img/" + file_name)
        return ImageTk.PhotoImage(image=image)