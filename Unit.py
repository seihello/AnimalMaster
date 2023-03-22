from abc import ABCMeta, abstractmethod
from enum import IntEnum
from Battle import Effectivity

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

    def set_initial_position(self, initial_position):
        self.initial_position = initial_position

    def set_move_direction(self, direction):
        self.move_direction = direction

    def reset_move_direction(self):
        self.move_direction = MoveDirection.STAY

    @abstractmethod
    def get_effectivity(self, opp_unit_kind):
        pass

class Mouse(Unit):

    def __init__(self, player_kind):
        super().__init__(player_kind, UnitKind.MOUSE)

    def get_effectivity(self, opp_unit_kind):
        if opp_unit_kind == UnitKind.MOUSE:
            return Effectivity.EVEN
        elif opp_unit_kind == UnitKind.CAT:
            return Effectivity.VERY_BAD
        elif opp_unit_kind == UnitKind.WOLF:
            return Effectivity.VERY_GOOD
        elif opp_unit_kind == UnitKind.HUMAN:
            return Effectivity.BAD


class Cat(Unit):

    def __init__(self, player_kind):
        super().__init__(player_kind, UnitKind.CAT)

    def get_effectivity(self, opp_unit_kind):
        if opp_unit_kind == UnitKind.MOUSE:
            return Effectivity.VERY_GOOD
        elif opp_unit_kind == UnitKind.CAT:
            return Effectivity.EVEN
        elif opp_unit_kind == UnitKind.WOLF:
            return Effectivity.VERY_BAD
        elif opp_unit_kind == UnitKind.HUMAN:
            return Effectivity.BAD

class Wolf(Unit):

    def __init__(self, player_kind):
        super().__init__(player_kind, UnitKind.WOLF)

    def get_effectivity(self, opp_unit_kind):
        if opp_unit_kind == UnitKind.MOUSE:
            return Effectivity.VERY_BAD
        elif opp_unit_kind == UnitKind.CAT:
            return Effectivity.VERY_GOOD
        elif opp_unit_kind == UnitKind.WOLF:
            return Effectivity.EVEN
        elif opp_unit_kind == UnitKind.HUMAN:
            return Effectivity.BAD

class Human(Unit):

    def __init__(self, player_kind):
        super().__init__(player_kind, UnitKind.HUMAN)

    def get_effectivity(self, opp_unit_kind):
        if opp_unit_kind == UnitKind.MOUSE:
            return Effectivity.GOOD
        elif opp_unit_kind == UnitKind.CAT:
            return Effectivity.GOOD
        elif opp_unit_kind == UnitKind.WOLF:
            return Effectivity.GOOD
        elif opp_unit_kind == UnitKind.HUMAN:
            return Effectivity.EVEN