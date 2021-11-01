import random
from enum import IntEnum
from Common import Common
from GameManager import GameManager
from Player import PlayerKind, Player
from GameInfo import GameInfo
from GameEnd import GameResult
from AppFrame import AppFrame
from StatusCanvas import StatusCanvas

# 使用する戦略クラス(Playerを継承したクラス)をimportする
from SamplePlayer1 import SamplePlayer1
from SamplePlayer2 import SamplePlayer2

# アプリ状態
class AppStatus(IntEnum):
    PLAYING             = 1    # 対戦中
    WAITING_NEW_GAME    = 2    # 対戦開始待ち
    RESULT              = 3    # 対戦終了(結果表示)

# @class    アプリクラス
# @brief    指定した回数の対戦を管理する
class App:

    # @brief    コンストラクタ
    # @param    root     Tkinterのrootオブジェクト
    def __init__(self, root):

        # rootをメンバにセット
        self._root = root

        # オブジェクトを初期化
        self._game_manager = None
        self._game_info = GameInfo()

        # プレイヤーの作成
        ### ゲームに使用するPlayerクラスを変えたい場合、ここを変更すること ###
        lower_player = SamplePlayer1(PlayerKind.LOWER)
        upper_player = SamplePlayer2(PlayerKind.UPPER)
        self._players = (lower_player, upper_player)

        # Playerクラスを継承していない場合強制終了
        if not issubclass(type(lower_player), Player):
            print("lower_player is not Player")
            exit()
        elif not issubclass(type(upper_player), Player):
            print("upper_player is not Player")
            exit()

        # アプリ状態は"対戦開始待ち"
        self._status = AppStatus.WAITING_NEW_GAME

        # GUIコンポーネントの作成
        self.app_frame = AppFrame(root)
        self.app_frame.place(x=0, y=0)
        self._status_canvas = StatusCanvas(self.app_frame)
        self._status_canvas.place(x=0, y=0)

        # ステータス画面に初期値をセット
        self._status_canvas.draw_player_name(self._players[PlayerKind.LOWER].get_name(), self._players[PlayerKind.UPPER].get_name())
        self._status_canvas.update_win_count(0, 0, 0)

    # @brief    アプリを開始する(設定回数分ゲームを繰り返す)
    # @details  最初だけ仮想的にクリックさせて1回目の対戦を開始する
    def start(self):

        # 乱暴だが共通化するためにクリックされたことにする
        self.on_clicked("<Button-1>")

    # @brief    画面がクリックされたときのハンドラ
    # @details  対戦開始待ちの場合、対戦を開始する
    #           対戦中の場合、盤面を進める
    #           指定した回数分対戦が終わっている場合、何もしない
    def on_clicked(self, event):

        # アプリ状態によって処理を分ける
        # 対戦開始待ちの場合、新しいゲームを開始する
        if self._status == AppStatus.WAITING_NEW_GAME:
            self._game_manager = GameManager(self, self._players[PlayerKind.LOWER], self._players[PlayerKind.UPPER])
            game_end_result = self._game_manager.start_game(self._game_info, self._get_next_first_turn_player(self._game_info.game_count))

            # 決着がついた場合は対戦終了処理
            if game_end_result != GameResult.NOT_COMPLETE:
                self._finish_game(game_end_result)
            # それ以外は対戦中に遷移
            else:
                self._status = AppStatus.PLAYING

        # 対戦中の場合、盤面を1ターン進める
        elif self._status == AppStatus.PLAYING:

            # 1ターン進める
            game_end_result = self._game_manager.step()

            # 決着がついた場合は対戦終了処理
            if game_end_result != GameResult.NOT_COMPLETE:
                self._finish_game(game_end_result)

    # @brief    対戦終了処理
    # @details  結果の表示と勝敗数の更新を行う
    #           指定した回数対戦が完了していない場合、アプリ状態を"対戦開始待ち"にする
    #           指定した回数対戦が完了した場合、アプリ状態を"結果表示"にする
    # @param    game_end_result(GameResult) 対戦結果
    # @return   なし
    def _finish_game(self, game_end_result):

        # 結果をダイアログ表示
        self.app_frame.show_result(game_end_result, self._players[PlayerKind.LOWER].get_name(),
                                   self._players[PlayerKind.UPPER].get_name())

        # 対戦数と勝利数情報を更新
        self._game_info.game_count += 1
        if game_end_result == GameResult.LOWER_WIN:
            self._game_info.win_count[PlayerKind.LOWER] += 1
        elif game_end_result == GameResult.UPPER_WIN:
            self._game_info.win_count[PlayerKind.UPPER] += 1

        # ステータス画面の勝利数を更新
        self._status_canvas.update_win_count(self._game_info.win_count[PlayerKind.LOWER],
                                            self._game_info.win_count[PlayerKind.UPPER], 0)

        # 対戦がまだ残っていれば継続
        # 設定回数の対戦が終了していたら次の対戦に進まないように状態をセット
        if self._game_info.game_count < Common.MAX_GAME_COUNT:
            self._status = AppStatus.WAITING_NEW_GAME
        else:
            self._status = AppStatus.RESULT

    # @brief    先攻のプレイヤー種別を求める
    # @details  奇数回目は下側が先攻、偶数回目は上側が先攻になるようにする
    #           ただし、最後の対戦はランダムで先攻を決める
    # @param    (int)game_count 現時点で対戦が完了した回数
    # @return   (PlayerKind)    先攻のプレイヤー種別
    def _get_next_first_turn_player(self, game_count):

        # 最後の対戦はランダムで決定
        if game_count == Common.MAX_GAME_COUNT - 1:
            if random.randint(1, 2) == 1:
                return PlayerKind.LOWER
            else:
                return PlayerKind.UPPER

        # それ以外は、奇数回目は下側が先攻、偶数回目は上側が先攻
        else:
            if game_count % 2 == 0:
                return PlayerKind.LOWER
            elif game_count % 2 == 1:
                return PlayerKind.UPPER
