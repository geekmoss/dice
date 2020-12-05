from .Player import Player
from .Combination import Combination


class Game:
    def __init__(self, points_to_win: int = 10000):
        self.player1 = Player(Player.STATE_CAN_ROLL, self)
        self.player2 = Player(Player.STATE_END_OR_NO_OPT, self)

        self.on_turn = self.player1
        self.points_to_win = points_to_win
        pass

    def player_on_turn(self):
        return self.on_turn

    def can_roll(self):
        return self.on_turn.player_state == Player.STATE_CAN_ROLL

    def can_pick(self):
        return self.on_turn.player_state == Player.STATE_PICKING

    def roll(self):
        return self.on_turn.roll_active_dice()

    def available_combos(self):
        return self.on_turn.get_combos()

    def pick_combo(self, c: Combination):
        return self.on_turn.pick_combo(c)

    def pick_by_values(self, values: tuple):
        c = self.on_turn.find_dice_for_combo(values)
        if c is False or c.points == 0:
            return False

        return self.on_turn.pick_combo(c)

    def confirm_pick(self):
        return self.on_turn.confirm_pick()

    def cancel_pick(self):
        return self.on_turn.cancel_pick()

    def end_turn(self):
        self.on_turn.end_turn()

        self.on_turn = self.player1 if self.on_turn == self.player2 else self.player2

        self.on_turn.new_turn()
        pass

    def is_winner(self):
        return self.player1.points >= self.points_to_win or self.player2.points >= self.points_to_win

    def __repr__(self):
        return f"Player 1 on turn" if self.on_turn == self.player1 else f"Player 2 on turn"
    pass
