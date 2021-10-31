import random
from enum import IntEnum
from Common import Common
from Unit import UnitKind

# 駒の相性
class Effectivity(IntEnum):
    VERY_GOOD   = 1   # 強い
    GOOD        = 2   # やや強い
    EVEN        = 3   # 互角(同じ種類)
    BAD         = 4   # やや弱い
    VERY_BAD    = 5   # 弱い

class BattleResult(IntEnum):
    DRAW        = 0   # 引き分け
    UNIT1_WIN   = 1   # ユニット1の勝利
    UNIT2_WIN   = 2   # ユニット2の勝利

class Battle:
    def __init__(self):
        pass

    # 戦闘する
    # 2つのユニット種別を受け取り、対戦させてどちらが勝利か返す
    def battle(self, unit_kind1, unit_kind2):

        # ユニット1から見たユニット2の相性を取得
        effectivity = self.get_effectivity(unit_kind1, unit_kind2)

        # 相性が互角なら引き分け
        if effectivity == Effectivity.EVEN:
            return BattleResult.DRAW

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
            return BattleResult.UNIT1_WIN
        else:
            return BattleResult.UNIT2_WIN

    # ユニット1から見たユニット2に対する相性を返す
    def get_effectivity(self, unit_kind1, unit_kind2):

        # 自分(ユニット1)と相手(ユニット2)が同じ種類の場合、相性は互角
        if unit_kind1 == unit_kind2:
            return Effectivity.EVEN

        # 自分が人間の場合、どの駒に対しても相性はやや強い
        # 人間同士の場合は上の判定に入っているためここには入らない
        elif unit_kind1 == UnitKind.HUMAN:
            return Effectivity.GOOD

        # 自分が人間以外の場合
        elif unit_kind1 != UnitKind.HUMAN:
            # 人間に対しては相性がやや弱い
            if unit_kind2 == UnitKind.HUMAN:
                return Effectivity.VERY_BAD

            # 相手も人間でない場合
            elif unit_kind2 != UnitKind.HUMAN:

                # 自分がネズミの場合、オオカミには強く、ネコには弱い
                if unit_kind1 == UnitKind.MOUSE:
                    if unit_kind2 == UnitKind.WOLF:
                        return Effectivity.VERY_GOOD
                    elif unit_kind2 == UnitKind.CAT:
                        return Effectivity.VERY_BAD

                # 自分がネコの場合、ネズミには強く、オオカミには弱い
                elif unit_kind1 == UnitKind.CAT:
                    if unit_kind2 == UnitKind.MOUSE:
                        return Effectivity.VERY_GOOD
                    elif unit_kind2 == UnitKind.WOLF:
                        return Effectivity.VERY_BAD

                # 自分がオオカミの場合、ネコには強くネズミには弱い
                elif unit_kind1 == UnitKind.WOLF:
                    if unit_kind2 == UnitKind.CAT:
                        return Effectivity.VERY_GOOD
                    elif unit_kind2 == UnitKind.MOUSE:
                        return Effectivity.VERY_BAD