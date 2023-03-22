import random
from enum import IntEnum
from Common import Common

# 駒の相性
class Effectivity(IntEnum):
    VERY_GOOD   = 1   # 強い
    GOOD        = 2   # やや強い
    EVEN        = 3   # 互角(同じ種類)
    BAD         = 4   # やや弱い
    VERY_BAD    = 5   # 弱い


class Battle:
    def __init__(self):
        pass

    # 戦闘する
    # 2つのユニットを受け取り、対戦させて負けた方を除去する
    def battle(self, my_unit, opp_unit):

        # ユニット1から見たユニット2の相性を取得
        effectivity = my_unit.get_effectivity(opp_unit.unit_kind)

        # 相性が互角なら引き分けで両者除去
        if effectivity == Effectivity.EVEN:
            my_unit.is_living = False
            opp_unit.is_living = False
            return

        # 相性がそれ以外なら、相性に基づいて勝利確率をセット
        if effectivity == Effectivity.VERY_GOOD:
            winning_percentage = Common.WINNING_PERCENTAGE_VERY_GOOD
        elif effectivity == Effectivity.GOOD:
            winning_percentage = Common.WINNING_PERCENTAGE_GOOD
        elif effectivity == Effectivity.BAD:
            winning_percentage = 100 - Common.WINNING_PERCENTAGE_GOOD
        elif effectivity == Effectivity.VERY_BAD:
            winning_percentage = 100 - Common.WINNING_PERCENTAGE_VERY_GOOD

        # 乱数を発生させ、勝利確率をもとに勝ち負けを決定する
        if random.randint(1, 100) <= winning_percentage:
            opp_unit.is_living = False
        else:
            my_unit.is_living = False
