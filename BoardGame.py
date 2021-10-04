from GameMaster import GameMaster
from Player import SamplePlayer1, SamplePlayer2, PlayerKind
from AppDisplay import AppDisplay
from enum import IntEnum
from GameMaster import GameResult

class GameStatus(IntEnum):
    TOP = 0
    PLAYING = 1
    WAITING_NEW_GAME = 2
    RESULT = 3

class BoardGame:

    def __init__(self, root):
        self.app_display = AppDisplay(root)
        self.game_master = None

        # ここでセットしたPlayerがゲームで使用される
        self.lower_player = SamplePlayer1(PlayerKind.LOWER)
        self.upper_player = SamplePlayer2(PlayerKind.UPPER)

        self.status = GameStatus.WAITING_NEW_GAME

    def start(self):

        self.app_display.create_game_display()
        self.app_display.game_display.board_canvas.bind('<Button-1>', self.on_clicked)

        self.game_master = GameMaster(self.app_display.game_display, self.lower_player, self.upper_player, PlayerKind.LOWER)
        self.game_master.start_game()

        self.status = GameStatus.PLAYING

    def on_clicked(self, event):
        
        if self.status == GameStatus.PLAYING:
            game_end_result = self.game_master.step()
            if game_end_result != GameResult.NOT_COMPLETE:
                self.app_display.show_result(game_end_result, self.lower_player, self.upper_player)
                self.status = GameStatus.WAITING_NEW_GAME

        elif self.status == GameStatus.WAITING_NEW_GAME:

            self.start()


