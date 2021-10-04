from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

from Common import Common
from Unit import UnitKind
from Player import PlayerKind
from GameMaster import GameResult

class GameDisplay:
    def __init__(self, app_frame):

        self.app_frame = app_frame
        self.player_colors = {PlayerKind.LOWER : "red", PlayerKind.UPPER : "#0F6FF7"}

        back_image = Image.open('lawn.png')
        self.back_image = ImageTk.PhotoImage(image=back_image)

        self.board_canvas = tk.Canvas(self.app_frame, width=Common.WINDOW_WIDTH, height=Common.WINDOW_HEIGHT,
                                      highlightthickness=0, background='White')
        self.board_canvas.place(x=0, y=0)


        # 背景画像をセット
        self.board_canvas.create_image(0, 0, image=self.back_image, anchor='nw')

        for i in range(9):
            self.board_canvas.create_line(Common.MASS_SIZE * i, 0, Common.MASS_SIZE * i, Common.WINDOW_WIDTH,
                                          fill='Grey')
        for j in range(9):
            self.board_canvas.create_line(0, Common.MASS_SIZE * j, Common.WINDOW_HEIGHT, Common.MASS_SIZE * j,
                                          fill='Grey')

        base_lower_image = self.get_image("base_lower.png")
        base_upper_image = self.get_image("base_upper.png")
        self.base_images = (base_lower_image, base_upper_image)

        self.board_canvas.create_image(
            Common.MASS_SIZE * 3, Common.MASS_SIZE * 6,
            image=base_lower_image, anchor='nw')
        self.board_canvas.create_image(
            Common.MASS_SIZE * 3, 0,
            image=base_upper_image, anchor='nw')

        # self.board_canvas.create_rectangle(Common.MASS_SIZE * 3, 0, Common.MASS_SIZE * 3 + Common.MASS_SIZE, Common.MASS_SIZE,
        #                                    fill=self.player_colors[PlayerKind.UPPER])
        # self.board_canvas.create_rectangle(Common.MASS_SIZE * 3, Common.MASS_SIZE * 6, Common.MASS_SIZE * 3 + Common.MASS_SIZE, Common.MASS_SIZE * 6 + Common.MASS_SIZE,
        #                                    fill=self.player_colors[PlayerKind.LOWER])

        mouse_lower_image = self.get_image("mouse_lower.png")
        cat_lower_image = self.get_image("cat_lower.png")
        wolf_lower_image = self.get_image("wolf_lower.png")
        human_lower_image = self.get_image("human_lower.png")

        lower_unit_images = (mouse_lower_image, cat_lower_image, wolf_lower_image, human_lower_image)

        mouse_upper_image = self.get_image("mouse_upper.png")
        cat_upper_image = self.get_image("cat_upper.png")
        wolf_upper_image = self.get_image("wolf_upper.png")
        human_upper_image = self.get_image("human_upper.png")

        upper_unit_images = (mouse_upper_image, cat_upper_image, wolf_upper_image, human_upper_image)

        self.unit_images = (lower_unit_images, upper_unit_images)

        unit_circle_lower_image = self.get_image("unit_circle_lower.png")
        unit_circle_upper_image = self.get_image("unit_circle_upper.png")
        self.unit_circle_images = (unit_circle_lower_image, unit_circle_upper_image)

        self.units_id = []

        self.transparent_images = []

    def draw_units(self, units):

        for unit in units:

            if unit.is_living == True:

                # id = self.board_canvas.create_oval(
                #     unit.x * Common.MASS_SIZE + 10, unit.y * Common.MASS_SIZE + 30,
                #     unit.x * Common.MASS_SIZE + Common.MASS_SIZE - 10, unit.y * Common.MASS_SIZE + Common.MASS_SIZE - 10,
                #     fill=self.player_colors[unit.player_kind])
                id = self.board_canvas.create_image(
                    unit.x * Common.MASS_SIZE + 10, unit.y * Common.MASS_SIZE + 30,
                    image=self.unit_circle_images[unit.player_kind], anchor='nw')
                self.units_id.append(id)

                id = self.board_canvas.create_image(
                    unit.x * Common.MASS_SIZE, unit.y * Common.MASS_SIZE - 10,
                    image=self.unit_images[unit.player_kind][unit.unit_kind], anchor='nw')
                self.units_id.append(id)

    def clear_units(self):

        for id in self.units_id:
            self.board_canvas.delete(id)

    def get_image(self, file_name):
        image = Image.open(file_name)
        return ImageTk.PhotoImage(image=image)

