import random
from enum import IntEnum
from Unit import Unit, UnitKind
from Common import Common

class Effectivity(IntEnum):
    VERY_GOOD = 1
    GOOD = 2
    EVEN = 3
    BAD = 4
    VERY_BAD = 5

class BattleResult(IntEnum):
    DRAW = 0
    UNIT1_WIN = 1
    UNIT2_WIN = 2

class Battle:
    def __init__(self):
        pass

    @staticmethod
    def battle(unit_kind1, unit_kind2):

        effectivity = Battle.get_effectivity(unit_kind1, unit_kind2)

        if effectivity == Effectivity.EVEN:
            return BattleResult.DRAW

        if effectivity == Effectivity.VERY_GOOD:
            winning_percentage = Common.WINNING_PERCENTAGE_VERY_GOOD
        elif effectivity == Effectivity.GOOD:
            winning_percentage = Common.WINNING_PERCENTAGE_GOOD
        elif effectivity == Effectivity.BAD:
            winning_percentage = 100 - Common.WINNING_PERCENTAGE_GOOD
        elif effectivity == Effectivity.VERY_BAD:
            winning_percentage = 100 - Common.WINNING_PERCENTAGE_VERY_GOOD

        if random.randint(1, 100) <= winning_percentage:
            return BattleResult.UNIT1_WIN
        else:
            return BattleResult.UNIT2_WIN

    # 引数1の引数2に対する相性を返す
    @staticmethod
    def get_effectivity(unit_kind1, unit_kind2):

        # 自分と相手が同じ種類
        if unit_kind1 == unit_kind2:
            return Effectivity.EVEN

        # 自分が人間
        elif unit_kind1 == UnitKind.HUMAN:
            return Effectivity.GOOD

        # 自分が動物
        else:
            if unit_kind2 == UnitKind.HUMAN:
                return Effectivity.VERY_BAD

            if unit_kind1 == UnitKind.MOUSE:
                if unit_kind2 == UnitKind.WOLF:
                    return Effectivity.VERY_GOOD
                elif unit_kind2 == UnitKind.CAT:
                    return Effectivity.VERY_BAD

            elif unit_kind1 == UnitKind.CAT:
                if unit_kind2 == UnitKind.MOUSE:
                    return Effectivity.VERY_GOOD
                elif unit_kind2 == UnitKind.WOLF:
                    return Effectivity.VERY_BAD

            elif unit_kind1 == UnitKind.WOLF:
                if unit_kind2 == UnitKind.CAT:
                    return Effectivity.VERY_GOOD
                elif unit_kind2 == UnitKind.MOUSE:
                    return Effectivity.VERY_BAD