from .Dice import Dice
from .Combination import Combination
from itertools import combinations


class Player:
    STATE_CAN_ROLL = 1
    STATE_PICKING = 2
    STATE_END_OR_NO_OPT = 3

    def __init__(self, init_state=STATE_CAN_ROLL, game=None):
        self.dice = [Dice(index=i) for i in range(6)]
        self.stored_dice = []
        self.active_dice = self.dice.copy()
        self.picked_dice = []
        self.active_indexes = []
        self.picked_indexes = []
        self.stored_indexes = []
        self.points = 0
        self.picked_points = 0
        self.points_progress = []
        self.player_state = init_state
        self.game = game
        pass

    def roll_active_dice(self):
        if self.player_state != self.STATE_CAN_ROLL:
            return False

        [d.roll() for d in self.active_dice]

        if not self.get_combos():
            self.player_state = self.STATE_END_OR_NO_OPT
            self.picked_points = 0
            pass
        else:
            self.player_state = self.STATE_PICKING
            pass

        return self.active_dice

    def get_combos(self):
        combos = []

        # Pick 50 or 100 points
        for d in self.active_dice:
            if d.state in (1, 5):
                combos.append(Combination((d,)))
                pass
            pass

        # Pick same numbers
        _combos = []
        for n in range(1, 7):
            _all = [d for d in self.active_dice if d.state == n]
            if len(_all) < 3:
                continue
            
            for i in range(3, len(_all) + 1):
                for c in combinations(_all, i):
                    _combos.append(Combination(c))
                pass
            pass

        combos += list(set(_combos))

        # Pick sequence
        _combos = []
        values = [d.state for d in self.active_dice]
        if (1 in values) and (2 in values) and (3 in values) and (4 in values) and (5 in values):
            if 6 in values:
                combos.append(
                    Combination(tuple(sorted([d for d in self.active_dice], key=lambda x: x.state)))
                )
                pass
            else:
                sequence = []
                _sequence_values = set()
                for d in self.active_dice:
                    if d.state in _sequence_values:
                        continue

                    _sequence_values.add(d.state)
                    sequence.append(d)
                    pass

                sequence.sort(key=lambda x: x.state)
                combos.append(Combination(tuple(sequence)))
                pass
            pass

        combos += list(set(_combos))

        return combos

    def pick_combo(self, combo: Combination):
        if combo not in self.get_combos():
            return False

        for d in combo.dice:
            self.active_dice.remove(d)
            self.picked_dice.append(d)
            pass
        self.picked_points += combo.points
        pass

    def confirm_pick(self):
        self.stored_dice += self.picked_dice
        self.picked_dice = []

        if len(self.active_dice) == 0:
            self.active_dice = self.dice.copy()
            self.stored_dice = []

        self.player_state = self.STATE_CAN_ROLL
        pass

    def cancel_pick(self):
        self.active_dice += self.picked_dice
        self.picked_dice = []
        self.picked_points = 0
        pass

    def end_turn(self):
        self.points += self.picked_points
        self.points_progress.append(self.points)
        self.picked_points = 0

        self.player_state = self.STATE_END_OR_NO_OPT
        pass

    def new_turn(self):
        self.player_state = self.STATE_CAN_ROLL

        self.active_dice = self.dice.copy()

        self.picked_dice = []
        self.stored_dice = []
        pass

    def find_dice_for_combo(self, values: tuple):
        dice = []
        available_dice = self.active_dice.copy()
        for v in values:
            for d in available_dice:
                if d.state == v:
                    dice.append(d)
                    available_dice.remove(d)
                    pass
                if len(dice) == len(values):
                    break
                pass
            pass

        if len(dice) == len(values):
            return Combination(tuple(dice))

        return False

    def make_combo_by_indexes(self, indexes: list):
        dices = [d for d in self.dice if (d.index in indexes)]
        self.pick_combo(Combination(tuple(dices)))

    def __repr__(self):
        dice = ", ".join([f"{d.state}" for d in self.dice])
        return f"P: {self.points}, D: ({dice}), S: {self.player_state}"
    pass

