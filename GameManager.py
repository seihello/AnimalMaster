import copy
from Common import Common
from Unit import Human, Mouse, Cat, Wolf, MoveDirection
from Player import PlayerKind, Player
from Collision import Collision
from GameEnd import GameResult, GameEnd
from GameCanvas import GameCanvas

# 1回の対戦の管理クラス
class GameManager:

    # コンストラクタ
    def __init__(self, app, lower_player, upper_player):

        # 対戦に使用するプレイヤーのリスト
        # PlayerKind.LOWER(0)とPlayerKind.UPPER(1)をIndexに使ってアクセスする
        self.__players = (lower_player, upper_player)

        # 下側/上側のプレイヤーの駒リスト
        # PlayerKind.LOWER(0)とPlayerKind.UPPER(1)をIndexに使ってアクセスする
        self.__units = ()

        # 各種インスタンスの作成
        self.__collision = Collision()
        self.__game_end = GameEnd()

        # 現在の駒を動かす側のプレイヤー
        self.__current_turn_player = PlayerKind.LOWER

        # ターン数
        self.__turn = 0

        # 対戦画面を作成
        self.game_canvas = GameCanvas(app.app_frame)
        self.game_canvas.bind('<Button-1>', app.on_clicked)

    # ゲーム開始処理
    # 主には駒の初期配置
    def start_game(self, game_info, first_turn_player):

        # 先攻のプレイヤーが最初のターン(当たり前)
        self.__current_turn_player = first_turn_player

        # 下側/上側のプレイヤーの準備
        is_lower_successful, lower_units = self.prepare_player(PlayerKind.LOWER, game_info, first_turn_player)
        is_upper_successful, upper_units = self.prepare_player(PlayerKind.UPPER, game_info, first_turn_player)

        # 上側のプレイヤーでエラーが起こったら下側の勝利
        if is_lower_successful and not is_upper_successful:
            return GameResult.LOWER_WIN
        # 下側のプレイヤーでエラーが起こったら上側の勝利
        elif not is_lower_successful and is_upper_successful:
            return GameResult.UPPER_WIN
        # 両方のプレイヤーでエラーが起こったら引き分け
        elif not is_lower_successful and not is_upper_successful:
            return GameResult.DRAW

        # 準備が完了した駒リストをメンバにセット
        self.units = (lower_units, upper_units)

        # 駒を画面表示
        self.game_canvas.clear_units()
        self.game_canvas.draw_units(self.units[PlayerKind.LOWER])
        self.game_canvas.draw_units(self.units[PlayerKind.UPPER])

        return GameResult.NOT_COMPLETE

    # 一方のプレイヤーの準備
    # 対戦情報のセット、駒の作成、駒の配置、
    def prepare_player(self, player_kind, game_info, first_turn_player):

        # 引き分け回数を算出
        draw_count = game_info.game_count - game_info.win_count[PlayerKind.LOWER] - game_info.win_count[PlayerKind.UPPER]

        # Playerクラスに現在の対戦情報をセットする
        try:
            self.__players[player_kind].set_game_info(game_info.game_count,
                                                    game_info.win_count[player_kind],
                                                    game_info.win_count[Player.get_opp_player_kind(player_kind)],
                                                    draw_count,
                                                    first_turn_player == player_kind)
        # エラーを起こした場合はFalseを返して中断
        except Exception as exception:
            print(self.__players[self.__current_turn_player].name + " Exception : " + str(exception))
            return False, ()

        # 駒リストを作成
        units = self.create_initial_units(player_kind)

        # Playerクラスに駒の初期配置を決定してもらう
        try:
            self.__players[player_kind].deploy(units)
        except Exception as exception:
            print(self.__players[self.__current_turn_player].name + " Exception : " + str(exception))
            return False, ()

        # 初期配置IDから座標に変換する
        self.set_position_from_initial_position(units)

        # 上側のプレイヤーは座標を1回転
        if player_kind == PlayerKind.UPPER:
            self.rotate_position(units)

        # 同じ位置に複数の駒がある場合、1つを残して取り除く
        self.__collision.resolve_my_collision(units)

        # ID順に並べ替え
        rearranged_units = self.rearrange_units(units)

        return True, rearranged_units

    # 1ターン進める
    def step(self):

        # 行動する側の駒(my_units)、行動しない側の駒(opp_units)を準備する
        # 生きている駒だけ取得する(死んでいる駒はPlayerに渡さないようにする)
        my_units = self.get_living_units(self.__current_turn_player)
        opp_units = self.get_living_units(Player.get_opp_player_kind(self.__current_turn_player))

        # 勝手にデータを変更されてもいいようにコピーを渡すため、ここでコピーを作る
        my_units_copy = copy.deepcopy(my_units)
        opp_units_copy = copy.deepcopy(opp_units)

        # 上側のプレイヤーも下側目線で行動できるように座標をひっくり返す
        if self.__current_turn_player == PlayerKind.UPPER:
            self.rotate_position(my_units_copy)
            self.rotate_position(opp_units_copy)

        # 行動するプレイヤーに駒を渡して駒を動かす方向をセットしてもらう
        try:
            self.__players[self.__current_turn_player].move(my_units_copy, opp_units_copy)

        # エラーを発生させた場合は即敗北
        except Exception as exception:
            print(self.__players[self.__current_turn_player].name + " Exception : " + str(exception))

            if self.__current_turn_player == PlayerKind.LOWER:
                return GameResult.UPPER_WIN
            elif self.__current_turn_player == PlayerKind.UPPER:
                return GameResult.LOWER_WIN

        # 上側のプレイヤーは下側目線で行動できるよう座標をひっくり返したので、処理するときは元に戻す
        if self.__current_turn_player == PlayerKind.UPPER:
            self.rotate_move_direction(my_units_copy)

        # 一応長さをチェック
        if len(my_units_copy) != len(my_units):
            print("不正")

        # コピーしたオブジェクトから実オブジェクトに移動方向をコピー
        for i in range(len(my_units)):
            my_units[i].move_direction = my_units_copy[i].move_direction

        # 移動方向を元に座標を動かす
        self.move_units(my_units)

        # 盤外に飛び出した駒は除去する
        self.remove_outside_units(my_units)

        # 行動側の駒で同じ位置に複数の駒がある場合、1つを残して除去する
        self.__collision.resolve_my_collision(my_units)

        # 相手の駒と同じ位置にいる場合は戦闘してどちらか一方または両方を除去する
        self.__collision.resolve_opp_collision(my_units, opp_units)

        # ターン切替処理
        self.switch_turn()

        # ゲームの終了を判定する
        game_end_result = self.__game_end.check_game_end(self.units[PlayerKind.LOWER], self.units[PlayerKind.UPPER], self.__turn)

        # 駒を画面表示
        self.game_canvas.clear_units()
        self.game_canvas.draw_units(self.units[PlayerKind.LOWER])
        self.game_canvas.draw_units(self.units[PlayerKind.UPPER])

       # Debug用
       # self.show_status()

        return game_end_result

    # 移動方向によって座標を変更する
    def move_units(self, units):
        for unit in units:
            unit.move()

    # 盤外に飛び出した駒を除去する
    def remove_outside_units(self, units):
        for unit in units:
            if unit.x < 0 or Common.MASS_NUM - 1 < unit.x or unit.y < 0 or Common.MASS_NUM - 1 < unit.y:
                unit.is_living = False

    # ターン切替処理
    def switch_turn(self):

        # 移動方向をリセット
        self.reset_move_direction(self.units[self.__current_turn_player])

        # 現在ターンのプレイヤーを切り替える
        if self.__current_turn_player == PlayerKind.LOWER:
            self.__current_turn_player = PlayerKind.UPPER
        elif self.__current_turn_player == PlayerKind.UPPER:
            self.__current_turn_player = PlayerKind.LOWER

        # ターン数を増やす
        self.__turn += 1

        # 移動方向を反転する

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
    def set_position_from_initial_position(self, units):

        for unit in units:
            unit.set_position_from_initial_position()

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
            elif unit.move_direction == MoveDirection.DOWN_RIGHT:
                unit.move_direction = MoveDirection.UP_LEFT
            elif unit.move_direction == MoveDirection.DOWN:
                unit.move_direction = MoveDirection.UP
            elif unit.move_direction == MoveDirection.DOWN_LEFT:
                unit.move_direction = MoveDirection.UP_RIGHT
            elif unit.move_direction == MoveDirection.LEFT:
                unit.move_direction = MoveDirection.RIGHT
            elif unit.move_direction == MoveDirection.UP_LEFT:
                unit.move_direction = MoveDirection.DOWN_RIGHT

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
            unit.reset_move_direction()

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
