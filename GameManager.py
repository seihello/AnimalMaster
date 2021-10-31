from Unit import Human, Mouse, Cat, Wolf, UnitKind, MoveDirection
from Player import PlayerKind, Player
from Common import Common
import copy
from enum import IntEnum
from Collision import Collision
from GameCanvas import GameCanvas
from GameEnd import GameResult, GameEnd


# @class    1回の対戦の管理クラス
class GameManager:

    # @brief    コンストラクタ
    # @param    app     Appクラスのインスタンス(クリック通知用)
    # @param    lower_player    プレイヤークラス(下側)
    # @param    upper_player    プレイヤークラス(上側)
    def __init__(self, app, lower_player, upper_player):

        # 対戦に使用するプレイヤーのリスト
        # PlayerKind.LOWER(0)とPlayerKind.UPPER(1)をIndexに使ってアクセスする
        self.players = (lower_player, upper_player)

        # 各種インスタンスの作成
        self.collision = Collision()
        self.game_end = GameEnd()

        # 駒を作成してセット
        lower_units = self.create_initial_units(PlayerKind.LOWER)
        upper_units = self.create_initial_units(PlayerKind.UPPER)
        self.units = (lower_units, upper_units)

        # 対戦画面を作成
        self.game_canvas = GameCanvas(app.app_frame)
        self.game_canvas.bind('<Button-1>', app.on_clicked)

        # その他メンバ変数の定義を明示
        self.current_turn_player = PlayerKind.LOWER
        self.turn = 0

    # @brief    1回の対戦を開始する
    # @param    game_info   現時点の対戦
    def start_game(self, game_info, first_turn_player):

        # 先攻のプレイヤーが最初のターン(当たり前)
        self.current_turn_player = first_turn_player

        # Playerに現在の勝敗数と今回どちらが先攻の情報を渡す
        self.set_game_info(game_info, first_turn_player)

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
        self.collision.resolve_my_collision(self.units[PlayerKind.LOWER])
        self.collision.resolve_my_collision(self.units[PlayerKind.UPPER])

        # ID順に並べ替え
        rearranged_lower_units = self.rearrange_units(self.units[PlayerKind.LOWER])
        rearranged_upper_units = self.rearrange_units(self.units[PlayerKind.UPPER])
        self.units = (rearranged_lower_units, rearranged_upper_units)

        # ターン数をセット
        self.turn = 1

        # 駒を画面表示
        self.game_canvas.clear_units()
        self.game_canvas.draw_units(self.units[PlayerKind.LOWER])
        self.game_canvas.draw_units(self.units[PlayerKind.UPPER])



    # 1ターン進める
    def step(self):

        # 行動する側の駒(my_units)、行動しない側の駒(opp_units)を準備する
        # 生きている駒だけ取得する(死んでいる駒はPlayerに渡さないようにする)
        my_units = self.get_living_units(self.current_turn_player)
        opp_units = self.get_living_units(Player.get_opp_player_kind(self.current_turn_player))

        # 勝手にデータを変更されてもいいようにコピーを作る
        my_units_copy = copy.deepcopy(my_units)
        opp_units_copy = copy.deepcopy(opp_units)

        # 上側のプレイヤーも下側目線で行動できるように座標をひっくり返す
        if self.current_turn_player == PlayerKind.UPPER:
            self.rotate_position(my_units_copy)
            self.rotate_position(opp_units_copy)

        # 行動するプレイヤーに駒を渡して駒を動かす方向をセットしてもらう
        self.players[self.current_turn_player].move(my_units_copy, opp_units_copy)

        # 上側のプレイヤーは下側目線で行動できるよう座標をひっくり返したので、処理するときは元に戻す
        if self.current_turn_player == PlayerKind.UPPER:
            self.rotate_move_direction(my_units_copy)

        # オブジェクトごと上書きされないようにチェック
        if len(my_units_copy) != len(my_units):
            print("不正")

        # オブジェクトIDもチェックしたい

        # 移動方向をコピーしたオブジェクトから実オブジェクトにコピー
        for i in range(len(my_units)):
            my_units[i].move_direction = my_units_copy[i].move_direction

        # 移動方向を元に座標を変更
        self.move_units(my_units)

        # 盤外に飛び出した駒は除去する
        self.remove_outside_units(my_units)

        # 行動側の駒で同じ位置に複数の駒がある場合、1つを残して除去する
        self.collision.resolve_my_collision(my_units)

        # 相手の駒と同じ位置にいる場合は戦闘してどちらか一方または両方を除去する
        self.collision.resolve_opp_collision(my_units, opp_units)

        # ターン切替
        self.switch_turn()

        # 駒を画面表示
        self.game_canvas.clear_units()
        self.game_canvas.draw_units(self.units[PlayerKind.LOWER])
        self.game_canvas.draw_units(self.units[PlayerKind.UPPER])

        # ゲームの終了を判定する
        game_end_result = self.game_end.check_game_end(self.units[PlayerKind.LOWER], self.units[PlayerKind.UPPER],
                                                       self.turn)

        self.show_status()

        return game_end_result

    ### ここから下はprivate ###

    # Playerに現在の勝敗数と今回どちらが先攻の情報を渡す
    def set_game_info(self, game_info, first_turn_player):

        # 引き分け回数を算出
        draw_count = game_info.game_count - game_info.win_count[PlayerKind.LOWER] - game_info.win_count[
            PlayerKind.UPPER]

        # 各プレイヤーに駒の初期配置を決定してもらう
        self.players[PlayerKind.LOWER].set_game_info(game_info.game_count,
                                                     game_info.win_count[PlayerKind.LOWER],
                                                     game_info.win_count[PlayerKind.UPPER],
                                                     draw_count,
                                                     first_turn_player == PlayerKind.LOWER)
        self.players[PlayerKind.UPPER].set_game_info(game_info.game_count,
                                                     game_info.win_count[PlayerKind.UPPER],
                                                     game_info.win_count[PlayerKind.LOWER],
                                                     draw_count,
                                                     first_turn_player == PlayerKind.UPPER)

    # 移動方向によって座標を変更する
    def move_units(self, units):
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

    # 盤外に飛び出した駒を除去する
    def remove_outside_units(self, units):
        for unit in units:
            if unit.x < 0 or Common.MASS_NUM - 1 < unit.x or unit.y < 0 or Common.MASS_NUM - 1 < unit.y:
                unit.is_living = False

    # ターン切替処理
    def switch_turn(self):

        # 移動方向をリセット
        self.reset_move_direction(self.units[self.current_turn_player])

        # 現在ターンのプレイヤーを切り替える
        if self.current_turn_player == PlayerKind.LOWER:
            self.current_turn_player = PlayerKind.UPPER
        elif self.current_turn_player == PlayerKind.UPPER:
            self.current_turn_player = PlayerKind.LOWER

        # ターン数を増やす
        self.turn += 1

        # 移動方向を反転する

    ######## ここから下は雑用関数 ########

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

    # 初期位置IDから座標に変換する(下のプレイヤー目線の座標)
    def set_position_from_id(self, units):

        for unit in units:

            if unit.initial_position == 1:
                unit.x = 2
                unit.y = 5
            elif unit.initial_position == 2:
                unit.x = 4
                unit.y = 5
            elif unit.initial_position == 3:
                unit.x = 0
                unit.y = 5
            elif unit.initial_position == 4:
                unit.x = 6
                unit.y = 5
            elif unit.initial_position == 5:
                unit.x = 2
                unit.y = 6
            elif unit.initial_position == 6:
                unit.x = 4
                unit.y = 6
            elif unit.initial_position == 7:
                unit.x = 0
                unit.y = 6
            elif unit.initial_position == 8:
                unit.x = 6
                unit.y = 6
            else:
                unit.is_living = False

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

    # 座標を一回転させる
    def rotate_position(self, units):
        for unit in units:
            unit.x = Common.MASS_NUM - 1 - unit.x
            unit.y = Common.MASS_NUM - 1 - unit.y

    # 初期位置ID順に並べ替える
    def rearrange_units(self, units):

        rearranged_units = []

        for i in range(1, 9):
            for unit in units:
                if unit.initial_position == i:
                    rearranged_units.append(unit)

        return tuple(rearranged_units)

    # 移動方向を初期値に戻す
    def reset_move_direction(self, units):
        for unit in units:
            unit.move_direction = MoveDirection.STAY

    # 指定したプレイヤーの生きている駒一覧を取得する
    def get_living_units(self, player_kind):

        living_units = []

        for unit in self.units[player_kind]:
            if unit.is_living:
                living_units.append(unit)

        return tuple(living_units)

    # Debug用
    def show_status(self):
        print("LOWER UNITS")
        for unit in self.units[PlayerKind.LOWER]:
            print(str(unit.x) + ", " + str(unit.y) + ", " + str(unit.is_living))
        print("UPPER UNITS")
        for unit in self.units[PlayerKind.UPPER]:
            print(str(unit.x) + ", " + str(unit.y) + ", " + str(unit.is_living))
