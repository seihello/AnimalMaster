from Unit import Human, Mouse, Cat, Wolf, UnitKind, MoveDirection
from Player import PlayerKind
from Common import Common
import copy
from enum import IntEnum
from Battle import Battle, BattleResult



class GameResult(IntEnum):
    NOT_COMPLETE = 0
    DRAW = 1
    LOWER_WIN = 2
    UPPER_WIN = 3

class GameMaster:

    def __init__(self, gui, lower_player, upper_player, first_turn_player):
        self.gui = gui
        #self.processing = True
        self.current_turn = PlayerKind.LOWER

        self.is_playing = False

        # 一応明示
        self.current_turn = first_turn_player
        self.players = (lower_player, upper_player)

        # 駒を作成
        lower_units = self.create_initial_units(PlayerKind.LOWER)
        upper_units = self.create_initial_units(PlayerKind.UPPER)

        # 駒一覧に両プレイヤーの駒をセットする
        self.units = (lower_units, upper_units)

    def start_game(self):

        # 各プレイヤーに駒の初期配置を決定してもらう
        self.players[PlayerKind.LOWER].deploy(self.units[PlayerKind.LOWER])
        self.players[PlayerKind.UPPER].deploy(self.units[PlayerKind.UPPER])

        # オブジェクトIDチェック

        # 位置IDから座標に変換する
        self.set_position_from_id(self.units[PlayerKind.LOWER])
        self.set_position_from_id(self.units[PlayerKind.UPPER])

        # 上のプレイヤーは座標を1回転
        self.rotate_position(self.units[PlayerKind.UPPER])

        self.gui.clear_units()
        self.gui.draw_units(self.units[PlayerKind.LOWER])
        self.gui.draw_units(self.units[PlayerKind.UPPER])

        self.turn = 1
        self.is_playing = True


    def create_initial_units(self, player_kind):

        human1 = Human(player_kind)
        human2 = Human(player_kind)
        mouse1 = Mouse(player_kind)
        mouse2 = Mouse(player_kind)
        cat1 = Cat(player_kind)
        cat2 = Cat(player_kind)
        wolf1 = Wolf(player_kind)
        wolf2 = Wolf(player_kind)
        units = [human1, human2, mouse1, mouse2, cat1, cat2, wolf1, wolf2]

        return units

    # 位置IDから座標に変換する
    def set_position_from_id(self, units):

        for unit in units:

            # 仮想座標をセット
            if unit.initial_position == 1:
                unit.x = 2
                unit.y = 5
            if unit.initial_position == 2:
                unit.x = 4
                unit.y = 5
            if unit.initial_position == 3:
                unit.x = 0
                unit.y = 5
            if unit.initial_position == 4:
                unit.x = 6
                unit.y = 5
            if unit.initial_position == 5:
                unit.x = 2
                unit.y = 6
            if unit.initial_position == 6:
                unit.x = 4
                unit.y = 6
            if unit.initial_position == 7:
                unit.x = 0
                unit.y = 6
            if unit.initial_position == 8:
                unit.x = 6
                unit.y = 6

    def step(self):

        print("Step開始")

        my_units = self.get_living_units(self.current_turn)
        opp_units = self.get_living_units(self.get_opp_player(self.current_turn))

        my_units_copy = copy.deepcopy(my_units)
        opp_units_copy = copy.deepcopy(opp_units)

        if self.current_turn == PlayerKind.UPPER:
            self.rotate_position(my_units_copy)
            self.rotate_position(opp_units_copy)

        self.players[self.current_turn].move(my_units_copy, opp_units_copy)

        if self.current_turn == PlayerKind.UPPER:
            self.rotate_move_direction(my_units_copy)

        if len(my_units_copy) != len(my_units):
            print("不正")

        # オブジェクトIDもチェックしたい

        # 移動方向をマスターにコピー
        for i in range(len(my_units)):
            my_units[i].move_direction = my_units_copy[i].move_direction

        # 移動方向を元に座標を変更
        self.move(my_units)

        # 移動方向をリセット
        self.reset_move_direction(my_units)

        ########################

        self.remove_outside_units(my_units)

        self.resolve_collision(my_units)

        self.resolve_battle(my_units, opp_units)

        ########################

        # 描画処理
        self.gui.clear_units()
        self.gui.draw_units(self.units[PlayerKind.LOWER])
        self.gui.draw_units(self.units[PlayerKind.UPPER])

        game_end_result = self.check_game_end()

        self.show_status()

        # ターン切替
        self.switch_turn()

        return game_end_result

    # 指定したプレイヤーの生きている駒一覧を取得する
    def get_living_units(self, player_kind):
        living_units = []
        for unit in self.units[player_kind]:
            if unit.is_living:
                living_units.append(unit)

        # タプルに変換
        living_units = tuple(living_units)

        return living_units

    def get_opp_player(self, player_kind):
        if player_kind == PlayerKind.LOWER:
            return PlayerKind.UPPER
        elif player_kind == PlayerKind.UPPER:
            return PlayerKind.LOWER

    def rotate_position(self, units):
        for unit in units:
            unit.x = Common.MASS_NUM - 1 - unit.x
            unit.y = Common.MASS_NUM - 1 - unit.y

    def move(self, units):
        for unit in units:
            if unit.move_direction == MoveDirection.STAY:
                pass
            elif unit.move_direction == MoveDirection.UP:
                unit.y -= 1
            elif unit.move_direction == MoveDirection.UP_RIGHT:
                unit.x += 1
                unit.y -= 1
            elif unit.move_direction == MoveDirection.RIGHT:
                unit.x += 1
            elif unit.move_direction == MoveDirection.DONW_RIGHT:
                unit.x += 1
                unit.y += 1
            elif unit.move_direction == MoveDirection.DOWN:
                unit.y += 1
            elif unit.move_direction == MoveDirection.DOWN_LEFT:
                unit.x -= 1
                unit.y += 1
            elif unit.move_direction == MoveDirection.LEFT:
                unit.x -= 1
            elif unit.move_direction == MoveDirection.UP_LEFT:
                unit.x -= 1
                unit.y -= 1

    def rotate_move_direction(self, units):
        for unit in units:
            if unit.move_direction == MoveDirection.STAY:
                pass
            elif unit.move_direction == MoveDirection.UP:
                unit.move_direction = MoveDirection.DOWN
            elif unit.move_direction == MoveDirection.UP_RIGHT:
                unit.move_direction = MoveDirection.DOWN_LEFT
            elif unit.move_direction == MoveDirection.RIGHT:
                unit.move_direction = MoveDirection.LEFT
            elif unit.move_direction == MoveDirection.DONW_RIGHT:
                unit.move_direction = MoveDirection.UP_LEFT
            elif unit.move_direction == MoveDirection.DOWN:
                unit.move_direction = MoveDirection.UP
            elif unit.move_direction == MoveDirection.DOWN_LEFT:
                unit.move_direction = MoveDirection.UP_RIGHT
            elif unit.move_direction == MoveDirection.LEFT:
                unit.move_direction = MoveDirection.RIGHT
            elif unit.move_direction == MoveDirection.UP_LEFT:
                unit.move_direction = MoveDirection.DONW_RIGHT

    # 味方の駒同士で同じ位置にいる場合、1つを残して残りの駒を取り除く
    def resolve_collision(self, units):
        for i in range(0, len(units)):
            unit1 = units[i]
            for j in range(0, i):
                unit2 = units[j]

                if unit1.x == unit2.x and unit1.y == unit2.y:
                    unit1.is_living = False

    def resolve_battle(self, units1, units2):
        for unit1 in units1:
            for unit2 in units2:
                if unit1.x == unit2.x and unit1.y == unit2.y:
                    battle_result = Battle.battle(unit1.unit_kind, unit2.unit_kind)
                    print("戦闘発生：unit1 = " + str(unit1.unit_kind) + ", unit2 = " + str(unit2.unit_kind) + " 結果 = " + str(battle_result))
                    if battle_result == BattleResult.DRAW:
                        unit1.is_living = False
                        unit2.is_living = False
                    elif battle_result == BattleResult.UNIT1_WIN:
                        unit2.is_living = False
                    elif battle_result == BattleResult.UNIT2_WIN:
                        unit1.is_living = False


    def battle_all(self):
        pass

    def battle(self):
        pass

    # 勝ち負け引き分けを返す
    def check_game_end(self):

        # どちらかが敵陣マスに入ったらゲーム終了
        result = self.check_goal_arrival()
        if result != GameResult.NOT_COMPLETE:
            return result

        # 駒が全て死んだらゲーム終了
        result = self.check_unit_alive()
        if result != GameResult.NOT_COMPLETE:
            return result

        # 設定ターン数終わってゲームが終了しなかったらゲーム終了
        result = self.check_timeout()
        if result != GameResult.NOT_COMPLETE:
            return result

        return GameResult.NOT_COMPLETE

    def check_goal_arrival(self):
        for lower_unit in self.units[PlayerKind.LOWER]:
            if lower_unit.x == 3 and lower_unit.y == 0:
                return GameResult.LOWER_WIN
        for upper_unit in self.units[PlayerKind.UPPER]:
            if upper_unit.x == 3 and upper_unit.y == Common.MASS_NUM - 1:
                return GameResult.UPPER_WIN

        return GameResult.NOT_COMPLETE

    def check_unit_alive(self):
        lower_units_num = len(self.get_living_units(PlayerKind.LOWER))
        upper_units_num = len(self.get_living_units(PlayerKind.UPPER))
        if lower_units_num == 0 and upper_units_num == 0:
            return GameResult.DRAW
        elif upper_units_num == 0:
            return GameResult.LOWER_WIN
        elif lower_units_num == 0:
            return GameResult.UPPER_WIN
        else:
            return GameResult.NOT_COMPLETE

    def check_timeout(self):
        if Common.MAX_TURN <= self.turn:
            lower_units_num = len(self.get_living_units(PlayerKind.LOWER))
            upper_units_num = len(self.get_living_units(PlayerKind.UPPER))
            if upper_units_num < lower_units_num:
                return GameResult.LOWER_WIN
            elif lower_units_num < upper_units_num:
                return GameResult.UPPER_WIN
            else:
                return GameResult.DRAW
        else:
            return GameResult.NOT_COMPLETE



    def remove_outside_units(self, units):
        for unit in units:
            if unit.x < 0 or Common.MASS_NUM -1 < unit.x or unit.y < 0 or Common.MASS_NUM - 1 < unit.y:
                unit.is_living = False

    def reset_move_direction(self, units):
        for unit in units:
            unit.move_direction = MoveDirection.STAY

    def switch_turn(self):
        if self.current_turn == PlayerKind.LOWER:
            self.current_turn = PlayerKind.UPPER
        elif self.current_turn == PlayerKind.UPPER:
            self.current_turn = PlayerKind.LOWER

        self.turn += 1

    def show_status(self):
        print("LOWER UNITS")
        for unit in self.units[PlayerKind.LOWER]:
            print(str(unit.x) + ", " + str(unit.y) + ", " + str(unit.is_living))
        print("UPPER UNITS")
        for unit in self.units[PlayerKind.UPPER]:
            print(str(unit.x) + ", " + str(unit.y) + ", " + str(unit.is_living))