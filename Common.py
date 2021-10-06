from Player import PlayerKind

class Common:
    MASS_SIZE = 80
    MASS_NUM = 7



    GAME_CANVAS_WIDTH = MASS_SIZE * MASS_NUM
    GAME_CANVAS_HEIGHT = MASS_SIZE * MASS_NUM

    STATUS_CANVAS_WIDTH = GAME_CANVAS_WIDTH
    STATUS_CANVAS_HEIGHT = 80

    WINDOW_WIDTH = GAME_CANVAS_WIDTH
    WINDOW_HEIGHT = GAME_CANVAS_HEIGHT + STATUS_CANVAS_HEIGHT

    MAX_TURN = 30

    WINNING_PERCENTAGE_VERY_GOOD = 80
    WINNING_PERCENTAGE_GOOD = 60

    BATTLE_NUMBER = 5

    # @staticmethod
    # def to_actual_position(x, y, player_kind):
    #     # 下側のプレイヤーはそのまま返す
    #     if player_kind == PlayerKind.LOWER:
    #         return x, y
    #     # 上側のプレイヤーは上側から見た座標に変換して返す
    #     elif player_kind == PlayerKind.UPPER:
    #         actual_x = Common.MASS_NUM - 1 - x
    #         actual_y = Common.MASS_NUM - 1 - y
    #         return  actual_x, actual_y
    #     else:
    #         return -1, -1
