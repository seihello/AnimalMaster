from abc import ABCMeta, abstractmethod
from enum import IntEnum

# プレイヤー種別
class PlayerKind(IntEnum):
    LOWER = 0   # 上側のプレイヤー
    UPPER = 1   # 下側のプレイヤー

class Player(metaclass=ABCMeta):

    def __init__(self, player_kind):
        self.__player_kind = player_kind
        self.__name = self.__class__.__name__

    # 何試合目か、何勝しているか、
    @abstractmethod
    def set_game_info(self, game_count, win_count, lose_count, draw_count, is_first):
        pass

    # 各位置を呼び出して初期位置を決定すること
    @abstractmethod
    def deploy(self, my_units):
        pass

    # 各Pieceのmove関数を呼び出して移動する方向を決定すること
    @abstractmethod
    def move(self, my_units, opp_units):
        pass

    @staticmethod
    def get_opp_player_kind(player_kind):
        if player_kind == PlayerKind.LOWER:
            return PlayerKind.UPPER
        elif player_kind == PlayerKind.UPPER:
            return PlayerKind.LOWER

    def get_player_kind(self):
        return self.__player_kind

    def get_name(self):
        return self.__name




