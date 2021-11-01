from Battle import Battle

class Collision:

    def __init__(self):
        self._battle = Battle()

    # 味方同士の駒の重複を解消する
    # 味方の駒同士で同じ位置にいる場合、後で移動した駒を残し、先に移動していた駒は除去する
    def resolve_my_collision(self, units):
        for i in range(0, len(units)):
            unit1 = units[i]
            for j in range(0, i):
                unit2 = units[j]

                if unit1.x == unit2.x and unit1.y == unit2.y:
                    unit1.is_living = False

    # 味方と敵の駒の重複を解消する
    # 味方と敵で同じ位置にいる場合、戦闘を発生させてどちらか一方または両方を取り除く
    def resolve_opp_collision(self, my_units, opp_units):
        for my_unit in my_units:
            for opp_unit in opp_units:
                if my_unit.x == opp_unit.x and my_unit.y == opp_unit.y:
                    self._battle.battle(my_unit, opp_unit)
