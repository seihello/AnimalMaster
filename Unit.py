from abc import ABCMeta, abstractmethod
from enum import IntEnum

# 駒の種別
class UnitKind(IntEnum):
    MOUSE   = 0 # ネズミ
    CAT     = 1 # ネコ
    WOLF    = 2 # オオカミ
    HUMAN   = 3 # 人間

# 移動方向
class MoveDirection(IntEnum):
    STAY        = 0 # その場に留まる
    UP          = 1 # 上に移動
    UP_RIGHT    = 2 # 右上に移動
    RIGHT       = 3 # 右に移動
    DOWN_RIGHT  = 4 # 右下に移動
    DOWN        = 5 # 下に移動
    DOWN_LEFT   = 6 # 左下に移動
    LEFT        = 7 # 左に移動
    UP_LEFT     = 8 # 左上に移動

class Unit(metaclass=ABCMeta):

    def __init__(self, player_kind, unit_kind):
        # 扱いやすいように全てpublicとする

        # 駒種別
        self.unit_kind = unit_kind

        # 所属するプレイヤー種別
        self.player_kind = player_kind

        # 現在の座標
        self.x = -1
        self.y = -1

        # 生きているか
        self.is_living = True

        # 初期配置ID
        self.initial_position = -1

        # 移動方向
        self.move_direction = MoveDirection.STAY

    def set_initial_position(self, initial_position_id):
        self.initial_position = initial_position_id

    def set_move_direction(self, direction):
        self.move_direction = direction

    def reset_move_direction(self):
        self.move_direction = MoveDirection.STAY

    # 移動方向をもとに座標を変更する(下側目線)
    def move(self):
        if self.move_direction == MoveDirection.STAY:
            pass
        elif self.move_direction == MoveDirection.UP:
            self.y -= 1
        elif self.move_direction == MoveDirection.UP_RIGHT:
            self.x += 1
            self.y -= 1
        elif self.move_direction == MoveDirection.RIGHT:
            self.x += 1
        elif self.move_direction == MoveDirection.DOWN_RIGHT:
            self.x += 1
            self.y += 1
        elif self.move_direction == MoveDirection.DOWN:
            self.y += 1
        elif self.move_direction == MoveDirection.DOWN_LEFT:
            self.x -= 1
            self.y += 1
        elif self.move_direction == MoveDirection.LEFT:
            self.x -= 1
        elif self.move_direction == MoveDirection.UP_LEFT:
            self.x -= 1
            self.y -= 1

    # 初期配置IDから座標をセットする(下側目線)
    def set_position_from_initial_position(self):
        if self.initial_position == 1:
            self.x = 2
            self.y = 5
        elif self.initial_position == 2:
            self.x = 4
            self.y = 5
        elif self.initial_position == 3:
            self.x = 0
            self.y = 5
        elif self.initial_position == 4:
            self.x = 6
            self.y = 5
        elif self.initial_position == 5:
            self.x = 2
            self.y = 6
        elif self.initial_position == 6:
            self.x = 4
            self.y = 6
        elif self.initial_position == 7:
            self.x = 0
            self.y = 6
        elif self.initial_position == 8:
            self.x = 6
            self.y = 6
        else:
            self.is_living = False


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