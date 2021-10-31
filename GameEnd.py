from enum import IntEnum
from Player import PlayerKind
from Common import Common

# 1回の対戦結果
class GameResult(IntEnum):
    NOT_COMPLETE = 0
    DRAW = 1
    LOWER_WIN = 2
    UPPER_WIN = 3

class GameEnd:

    def __init__(self):
        pass

    # ゲーム終了を判定する
    def check_game_end(self, lower_units, upper_units, turn):

        # どちらかが敵陣マスに入ったらゲーム終了
        result = self.check_goal_arrival(lower_units, upper_units)
        if result != GameResult.NOT_COMPLETE:
            return result

        # 駒が全て死んだらゲーム終了
        result = self.check_unit_alive(lower_units, upper_units)
        if result != GameResult.NOT_COMPLETE:
            return result

        # 設定ターン数終わってゲームが終了しなかったらゲーム終了
        result = self.check_max_turn(lower_units, upper_units, turn)
        if result != GameResult.NOT_COMPLETE:
            return result

        return GameResult.NOT_COMPLETE

    # 敵陣営の進入によるゲーム終了を判定する
    def check_goal_arrival(self, lower_units, upper_units):
        for lower_unit in lower_units:
            if lower_unit.x == 3 and lower_unit.y == 0 and lower_unit.is_living:
                return GameResult.LOWER_WIN
        for upper_unit in upper_units:
            if upper_unit.x == 3 and upper_unit.y == Common.MASS_NUM - 1 and upper_unit.is_living:
                return GameResult.UPPER_WIN

        return GameResult.NOT_COMPLETE

    # 駒が全てなくなったことによるゲーム終了を判定する
    def check_unit_alive(self, lower_units, upper_units):
        lower_units_num = self.get_living_units_count(lower_units)
        upper_units_num = self.get_living_units_count(upper_units)
        if lower_units_num == 0 and upper_units_num == 0:
            return GameResult.DRAW
        elif upper_units_num == 0:
            return GameResult.LOWER_WIN
        elif lower_units_num == 0:
            return GameResult.UPPER_WIN
        else:
            return GameResult.NOT_COMPLETE

    # 設定ターン数完了したことによるゲーム終了を判定する
    def check_max_turn(self, lower_units, upper_units, turn):
        if Common.MAX_TURN <= turn:
            lower_units_num = self.get_living_units_count(lower_units)
            upper_units_num = self.get_living_units_count(upper_units)
            if upper_units_num < lower_units_num:
                return GameResult.LOWER_WIN
            elif lower_units_num < upper_units_num:
                return GameResult.UPPER_WIN
            else:
                return GameResult.DRAW
        else:
            return GameResult.NOT_COMPLETE

    def get_living_units_count(self, units):
        living_count = 0
        for unit in units:
            if unit.is_living:
                living_count += 1
        return living_count

