from Battle import Battle, BattleResult

class Collision:

    def __init__(self):
        self.battle = Battle()

    # 味方の駒同士で同じ位置にいる場合、1つを残して残りの駒を取り除く
    def resolve_my_collision(self, units):
        for i in range(0, len(units)):
            unit1 = units[i]
            for j in range(0, i):
                unit2 = units[j]

                if unit1.x == unit2.x and unit1.y == unit2.y:
                    unit1.is_living = False

    # 駒が重複した場合、戦闘を発生させてどちらか一方または両方を取り除く
    def resolve_opp_collision(self, units1, units2):
        for unit1 in units1:
            for unit2 in units2:
                if unit1.x == unit2.x and unit1.y == unit2.y:
                    battle_result = self.battle.battle(unit1.unit_kind, unit2.unit_kind)
                    print("戦闘発生：unit1 = " + str(unit1.unit_kind) + ", unit2 = " + str(unit2.unit_kind) + " 結果 = " + str(battle_result))
                    if battle_result == BattleResult.DRAW:
                        unit1.is_living = False
                        unit2.is_living = False
                    elif battle_result == BattleResult.UNIT1_WIN:
                        unit2.is_living = False
                    elif battle_result == BattleResult.UNIT2_WIN:
                        unit1.is_living = False