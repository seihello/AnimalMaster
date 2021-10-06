from GameMaster import GameMaster
from Player import SamplePlayer1, SamplePlayer2, PlayerKind
from AppFrame import AppFrame
from enum import IntEnum
from GameMaster import GameResult
from StatusCanvas import StatusCanvas
from Common import Common
from GameInfo import GameInfo

class GameStatus(IntEnum):
    TOP = 0
    PLAYING = 1
    WAITING_NEW_GAME = 2
    RESULT = 3

class BoardGame:

    def __init__(self, root):
        self.app_frame = AppFrame(root)
        self.app_frame.place(x=0, y=0)
        self.status_canvas = StatusCanvas(self.app_frame)
        self.status_canvas.place(x=0, y=0)

        self.game_master = None

        self.game_info = GameInfo()

        # ここでセットしたPlayerがゲームで使用される
        self.lower_player = SamplePlayer1(PlayerKind.LOWER)
        self.upper_player = SamplePlayer2(PlayerKind.UPPER)

        self.status_canvas.draw_player_name(self.lower_player.__class__.__name__, self.upper_player.__class__.__name__)
        self.status_canvas.update_win_count(0, 0, 0)

        self.status = GameStatus.WAITING_NEW_GAME

    def start(self):

        """Function

        Parameters
        ----------
        a : float
            First number

        b : float
            Second number

        Returns
        -------
        result_sum : float
            Sum of numbers

        result_prod : float
            Product of numbers
        """

        """Function

        Args:
            a (float): First number
            b (float): Second number

        Returns:
            result_sum (float): Sum of numbers
            result_prod (float): Product of numbers
        """



        self.game_master = GameMaster(self, self.lower_player, self.upper_player, PlayerKind.LOWER)
        self.game_master.start_game()

        self.game_info.game_count += 1

        self.status = GameStatus.PLAYING

    def on_clicked(self, event):
        
        if self.status == GameStatus.PLAYING:
            game_end_result = self.game_master.step()
            if game_end_result != GameResult.NOT_COMPLETE:
                self.app_frame.show_result(game_end_result, self.lower_player, self.upper_player)
                self.status = GameStatus.WAITING_NEW_GAME

                if game_end_result == GameResult.LOWER_WIN:
                    self.game_info.win_count[PlayerKind.LOWER] += 1
                elif game_end_result == GameResult.UPPER_WIN:
                    self.game_info.win_count[PlayerKind.UPPER] += 1

                self.status_canvas.update_win_count(self.game_info.win_count[PlayerKind.LOWER], self.game_info.win_count[PlayerKind.UPPER], 0)

                print(self.game_info.win_count[PlayerKind.LOWER])
                print(self.game_info.win_count[PlayerKind.UPPER])

        elif self.status == GameStatus.WAITING_NEW_GAME:

            self.start()


