from GameManager import GameManager
from Player import PlayerKind, Player, SamplePlayer1, SamplePlayer2
from AppFrame import AppFrame
from enum import IntEnum
from GameEnd import GameResult
from StatusCanvas import StatusCanvas
from Common import Common
from GameInfo import GameInfo
import random

# アプリ状態
# TOP→PLAYING→WAITING_NEW_GAME→PLAYING→WAITING_NEW_GAME→...→PLAYING→RESULTという遷移になる
class AppStatus(IntEnum):
    TOP = 0
    PLAYING = 1
    WAITING_NEW_GAME = 2
    RESULT = 3

class App:

    def __init__(self, root):

        self.root = root

        # とりあえず5回で固定
        self.MAX_GAME_COUNT = 5

        # オブジェクトを初期化
        self.game_manager = None
        self.game_info = GameInfo()

        # プレイヤーの作成
        ### ゲームに使用するPlayerクラスを変えたい場合、ここを変更してください ###
        lower_player = SamplePlayer1(PlayerKind.LOWER)
        upper_player = SamplePlayer2(PlayerKind.UPPER)
        self.players = (lower_player, upper_player)

        # Playerクラスを継承していない場合強制終了
        if not issubclass(type(lower_player), Player):
            print("lower_player is not Player")
            exit()
        elif not issubclass(type(upper_player), Player):
            print("upper_player is not Player")
            exit()

        # アプリ状態は"対戦開始待ち"
        self.status = AppStatus.WAITING_NEW_GAME

        # GUIコンポーネントの作成
        self.app_frame = AppFrame(root)
        self.app_frame.place(x=0, y=0)
        self.status_canvas = StatusCanvas(self.app_frame)
        self.status_canvas.place(x=0, y=0)

        # ステータス画面に初期値をセット
        self.status_canvas.draw_player_name(self.players[PlayerKind.LOWER].name, self.players[PlayerKind.UPPER].name)
        self.status_canvas.update_win_count(0, 0, 0)

    # アプリを開始する(設定回数分ゲームを繰り返す)
    def start(self):

        # 最初は下のプレイヤーが先攻
        self.start_game(PlayerKind.LOWER)

    # 1回の対戦を開始する
    # first_turn_player(PlayerKind): 先攻のプレイヤー
    def start_game(self, first_turn_player):

        # 1回分の対戦のオブジェクトを作成して開始
        self.game_manager = GameManager(self, self.players[PlayerKind.LOWER], self.players[PlayerKind.UPPER])
        self.game_manager.start_game(self.game_info, first_turn_player)

        # アプリ状態は"対戦中"
        self.status = AppStatus.PLAYING




    # 画面をクリックした時の処理
    def on_clicked(self, event):

        # 対戦中の場合
        if self.status == AppStatus.PLAYING:

            # 対戦管理クラスに通知して1ターン進める
            game_end_result = self.game_manager.step()

            # 1回の対戦が終了した場合
            if game_end_result != GameResult.NOT_COMPLETE:

                # 結果をダイアログ表示
                self.app_frame.show_result(game_end_result, self.players[PlayerKind.LOWER].name, self.players[PlayerKind.UPPER].name)

                # 対戦数と勝利数情報を更新
                self.game_info.game_count += 1
                if game_end_result == GameResult.LOWER_WIN:
                    self.game_info.win_count[PlayerKind.LOWER] += 1
                elif game_end_result == GameResult.UPPER_WIN:
                    self.game_info.win_count[PlayerKind.UPPER] += 1

                # ステータス画面の勝利数を更新
                self.status_canvas.update_win_count(self.game_info.win_count[PlayerKind.LOWER], self.game_info.win_count[PlayerKind.UPPER], 0)

                # 対戦がまだ残っていれば継続
                # 設定回数の対戦が終了していたら次の対戦に進まないように状態をセット
                if self.game_info.game_count < self.MAX_GAME_COUNT:
                    self.status = AppStatus.WAITING_NEW_GAME
                else:
                    self.status = AppStatus.RESULT

        # 対戦終了後、再度クリックされたら次の対戦を開始
        elif self.status == AppStatus.WAITING_NEW_GAME:
            self.start_game(self.get_next_first_turn_player(self.game_info.game_count))

    # 先攻のプレイヤーを求める
    def get_next_first_turn_player(self, game_count):

        # 最後の対戦はランダムで決定
        if game_count == self.MAX_GAME_COUNT - 1:
            if random.randint(1, 2) == 1:
                return PlayerKind.LOWER
            else:
                return PlayerKind.UPPER

        # 基本的には奇数回目は下側が先攻、偶数回目は上側が先攻
        else:
            if game_count % 2 == 0:
                return PlayerKind.LOWER
            elif game_count % 2 == 1:
                return PlayerKind.UPPER
