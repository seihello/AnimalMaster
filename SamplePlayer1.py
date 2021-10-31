from Player import Player
from Unit import MoveDirection

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

        #my_units[100].set_initial_position(50)

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

