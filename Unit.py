from abc import ABCMeta, abstractmethod
from enum import IntEnum

from PIL import Image, ImageTk

class UnitKind(IntEnum):
    MOUSE = 0
    CAT = 1
    WOLF = 2
    HUMAN = 3

class MoveDirection(IntEnum):
    STAY = 0
    UP = 1
    UP_RIGHT = 2
    RIGHT = 3
    DONW_RIGHT = 4
    DOWN = 5
    DOWN_LEFT = 6
    LEFT = 7
    UP_LEFT = 8


class Unit(metaclass=ABCMeta):

    def __init__(self, player_kind, unit_kind):
        self.player_kind = player_kind
        self.unit_kind = unit_kind
        self.x = -1
        self.y = -1
        self.initial_position = -1
        self.is_living = True

        self.move_direction = MoveDirection.STAY # 次に動く方向

    def set_initial_position(self, initial_position_id):
        self.initial_position = initial_position_id

    def set_move_direction(self, direction):
        self.move_direction = direction

    def reset_move_direction(self):
        self.move_direction = MoveDirection.STAY

    @staticmethod
    def is_animal(self, unit_kind):
        if unit_kind == UnitKind.CAT or unit_kind == UnitKind.MOUSE or unit_kind == UnitKind.WOLF:
            return True
        else:
            return False


class Mouse(Unit):

    def __init__(self, player_kind):
        super().__init__(player_kind, UnitKind.MOUSE)

class Cat(Unit):

    def __init__(self, player_kind):
        super().__init__(player_kind, UnitKind.CAT)

class Wolf(Unit):

    def __init__(self, player_kind):
        super().__init__(player_kind, UnitKind.WOLF)

class Human(Unit):

    def __init__(self, player_kind):
        super().__init__(player_kind, UnitKind.HUMAN)