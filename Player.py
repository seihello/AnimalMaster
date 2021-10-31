from enum import IntEnum
from Unit import MoveDirection
from abc import ABCMeta, abstractmethod

class PlayerKind(IntEnum):
    LOWER = 0
    UPPER = 1

class Player():

    def __init__(self, player_kind):
        self.player_kind = player_kind
        self.name = self.__class__.__name__

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

class SamplePlayer1(Player):

    def __init__(self, player_kind):
        super().__init__(player_kind)



    def set_game_info(self, game_count, win_count, lose_count, draw_count, is_first):
        self.turn = 0

    def deploy(self, my_units):
        # 初期値をセット
        my_units[0].set_initial_position(1)
        my_units[1].set_initial_position(2)
        my_units[2].set_initial_position(3)
        my_units[3].set_initial_position(4)
        my_units[4].set_initial_position(5)
        my_units[5].set_initial_position(6)
        my_units[6].set_initial_position(7)
        my_units[7].set_initial_position(8)

        return

    def move(self, my_units, opp_units):

        self.turn += 1

        if self.turn == 1:
            # 全員真上に進む
            my_units[0].set_move_direction(MoveDirection.UP)
            my_units[1].set_move_direction(MoveDirection.UP)
            my_units[2].set_move_direction(MoveDirection.UP)
            my_units[3].set_move_direction(MoveDirection.UP)
            my_units[4].set_move_direction(MoveDirection.RIGHT)
            my_units[5].set_move_direction(MoveDirection.LEFT)
            my_units[6].set_move_direction(MoveDirection.UP)
            my_units[7].set_move_direction(MoveDirection.UP)
        else:
            # 何もしない
            for my_unit in my_units:
                if my_unit.initial_position != 4 and my_unit.initial_position != 5:
                    my_unit.set_move_direction(MoveDirection.UP)

class SamplePlayer2(Player):

    def __init__(self, player_kind):
        super().__init__(player_kind)
        self.turn = 0

    def set_game_info(self, game_count, win_count, lose_count, draw_count, is_first):
        self.turn = 0

    def deploy(self, my_units):
        # 初期値をセット
        my_units[0].set_initial_position(1)
        my_units[1].set_initial_position(2)
        my_units[2].set_initial_position(3)
        my_units[3].set_initial_position(4)
        my_units[4].set_initial_position(5)
        my_units[5].set_initial_position(6)
        my_units[6].set_initial_position(7)
        my_units[7].set_initial_position(8)

        return

    def move(self, my_units, opp_units):

        self.turn += 1

        # 中央を攻める
        for my_unit in my_units:
            if my_unit.x < 3:
                my_unit.set_move_direction(MoveDirection.RIGHT)
            elif my_unit.x > 3:
                my_unit.set_move_direction(MoveDirection.LEFT)
            else:
                my_unit.set_move_direction(MoveDirection.UP)

class Yamada(Player):

    def __init__(self, player_kind):
        super().__init__(player_kind)

    def set_game_info(self, game_count, win_count, lose_count, draw_count, is_first):
        pass

    def deploy(self, my_units):
        # 初期値をセット
        my_units[0].set_initial_position(1)
        my_units[1].set_initial_position(1)
        my_units[2].set_initial_position(2)
        my_units[3].set_initial_position(2)
        my_units[4].set_initial_position(3)
        my_units[5].set_initial_position(4)
        my_units[6].set_initial_position(5)
        my_units[7].set_initial_position(6)

        return

    def move(self, my_units, opp_units):
        # 全員真上に進む
        for unit in my_units:
            unit.set_move_direction(MoveDirection.UP)









