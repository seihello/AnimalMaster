from Unit import Human, Mouse, Cat, Wolf, UnitKind, MoveDirection
from Player import PlayerKind
from Common import Common
import copy
from enum import IntEnum
from Battle import Battle, BattleResult
from GameCanvas import GameCanvas

class GameResult(IntEnum):
    NOT_COMPLETE = 0
    DRAW = 1
    LOWER_WIN = 2
    UPPER_WIN = 3

class GameMaster:

    def __init__(self, board_game, lower_player, upper_player, first_turn_player):

        self.game_canvas = GameCanvas(board_game.app_frame)
        self.game_canvas.bind('<Button-1>', board_game.on_clicked)

        self.current_turn = PlayerKind.LOWER

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

        # 同じ位置に複数の駒がある場合、1つを残して取り除く
        self.resolve_collision(self.units[PlayerKind.LOWER])
        self.resolve_collision(self.units[PlayerKind.UPPER])

        # ID順に並べ替え
        rearranged_lower_units = self.rearrange_units(self.units[PlayerKind.LOWER])
        rearranged_upper_units = self.rearrange_units(self.units[PlayerKind.UPPER])
        self.units = (rearranged_lower_units, rearranged_upper_units)

        # 駒を画面表示
        self.game_canvas.clear_units()
        self.game_canvas.draw_units(self.units[PlayerKind.LOWER])
        self.game_canvas.draw_units(self.units[PlayerKind.UPPER])

        # ターン数をセット
        self.turn = 1

    # 1ターン進める
    def step(self):

        print("Step開始")

        # 行動する側の駒(my_units)、行動しない側の駒(opp_units)を準備する
        # 生きている駒だけ取得する(死んでいる駒はPlayerに渡さないようにする)
        my_units = self.get_living_units(self.current_turn)
        opp_units = self.get_living_units(self.get_opp_player(self.current_turn))

        # 勝手にデータを変更されてもいいようにコピーを作る
        my_units_copy = copy.deepcopy(my_units)
        opp_units_copy = copy.deepcopy(opp_units)

        # 上側のプレイヤーも下側目線で行動できるように座標をひっくり返す
        if self.current_turn == PlayerKind.UPPER:
            self.rotate_position(my_units_copy)
            self.rotate_position(opp_units_copy)

        # 行動するプレイヤーに駒を渡して駒を動かす方向をセットしてもらう
        self.players[self.current_turn].move(my_units_copy, opp_units_copy)

        # 上側のプレイヤーは下側目線で行動できるよう座標をひっくり返したので、処理するときは元に戻す
        if self.current_turn == PlayerKind.UPPER:
            self.rotate_move_direction(my_units_copy)

        # オブジェクトごと上書きされないようにチェック
        if len(my_units_copy) != len(my_units):
            print("不正")

        # オブジェクトIDもチェックしたい

        # 移動方向をコピーしたオブジェクトから実オブジェクトにコピー
        for i in range(len(my_units)):
            my_units[i].move_direction = my_units_copy[i].move_direction

        # 移動方向を元に座標を変更
        self.move(my_units)

        # 移動方向をリセット
        self.reset_move_direction(my_units)

        # 盤外に飛び出した駒は除去する
        self.remove_outside_units(my_units)

        # 行動側の駒で同じ位置に複数の駒がある場合、1つを残して除去する
        self.resolve_collision(my_units)

        # 相手の駒と同じ位置にいる場合は戦闘してどちらか一方または両方を除去する
        self.resolve_battle(my_units, opp_units)

        # ターン切替
        self.switch_turn()

        # 駒を画面表示
        self.game_canvas.clear_units()
        self.game_canvas.draw_units(self.units[PlayerKind.LOWER])
        self.game_canvas.draw_units(self.units[PlayerKind.UPPER])

        # ゲームの終了を判定する
        game_end_result = self.check_game_end()

        # Debug用
        self.show_status()

        return game_end_result

    # 初期の駒を生成する(順番は適当)
    def create_initial_units(self, player_kind):

        human1 = Human(player_kind)
        human2 = Human(player_kind)
        mouse1 = Mouse(player_kind)
        mouse2 = Mouse(player_kind)
        cat1 = Cat(player_kind)
        cat2 = Cat(player_kind)
        wolf1 = Wolf(player_kind)
        wolf2 = Wolf(player_kind)

        units = (human1, human2, mouse1, mouse2, cat1, cat2, wolf1, wolf2)

        return units

    # 初期位置IDから座標に変換する
    def set_position_from_id(self, units):

        for unit in units:

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

    # 初期位置ID順に並べ替える
    def rearrange_units(self, units):

        rearranged_units = []

        for i in range(1, 9):
            for unit in units:
                if unit.initial_position == i:
                    rearranged_units.append(unit)

        return tuple(rearranged_units)

    # 指定したプレイヤーの生きている駒一覧を取得する
    def get_living_units(self, player_kind):

        living_units = []

        for unit in self.units[player_kind]:
            if unit.is_living:
                living_units.append(unit)

        return tuple(living_units)

    def get_opp_player(self, player_kind):
        if player_kind == PlayerKind.LOWER:
            return PlayerKind.UPPER
        elif player_kind == PlayerKind.UPPER:
            return PlayerKind.LOWER

    # 座標を一回転させる
    def rotate_position(self, units):
        for unit in units:
            unit.x = Common.MASS_NUM - 1 - unit.x
            unit.y = Common.MASS_NUM - 1 - unit.y

    # 移動方向によって座標を変更する
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

    # 移動方向を反転する
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

    # 駒が重複した場合、戦闘を発生させてどちらか一方または両方を取り除く
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

    # ゲーム終了を判定する
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

    # 敵陣営の進入によるゲーム終了を判定する
    def check_goal_arrival(self):
        for lower_unit in self.units[PlayerKind.LOWER]:
            if lower_unit.x == 3 and lower_unit.y == 0:
                return GameResult.LOWER_WIN
        for upper_unit in self.units[PlayerKind.UPPER]:
            if upper_unit.x == 3 and upper_unit.y == Common.MASS_NUM - 1:
                return GameResult.UPPER_WIN

        return GameResult.NOT_COMPLETE

    # 駒が全てなくなったことによるゲーム終了を判定する
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

    # 設定ターン数完了したことによるゲーム終了を判定する
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

    # 盤外に飛び出した駒を除去する
    def remove_outside_units(self, units):
        for unit in units:
            if unit.x < 0 or Common.MASS_NUM -1 < unit.x or unit.y < 0 or Common.MASS_NUM - 1 < unit.y:
                unit.is_living = False

    # 移動方向を初期値に戻す
    def reset_move_direction(self, units):
        for unit in units:
            unit.move_direction = MoveDirection.STAY

    # ターン切替処理
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