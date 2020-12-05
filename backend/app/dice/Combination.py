from .Dice import Dice
from typing import Tuple, Union


SINGLE = {1: 100, 5: 50}
MUL = {3: 1, 4: 2, 5: 4, 6: 8}
SEQUENCE_5 = 1000
SEQUENCE_6 = 2000


class Combination:
    def __init__(self, dice: Union[Dice, Tuple[Dice]]):
        self.dice = dice
        self.points = self.calculate_points()
        pass

    def calculate_points(self):
        if isinstance(self.dice, Dice):
            return SINGLE.get(self.dice.state, 0)
        elif len(self.dice) == 1:
            return SINGLE.get(self.dice[0].state, 0)

        values = [d.state for d in self.dice]

        n = values[0]
        i = values.count(n)
        if i >= 3:
            one_modification = 10 if n == 1 else 1
            return (n * 100 * one_modification) * MUL[i]

        return {
            (1, 2, 3, 4, 5): SEQUENCE_5,
            (1, 2, 3, 4, 5, 6): SEQUENCE_6
        }.get(tuple(set(values)), 0)

    def __repr__(self):
        if isinstance(self.dice, Dice):
            return f"{self.dice.state} for {self.points} points"

        s = ", ".join(f"{d.state}" for d in self.dice)
        return f"({s}) for {self.points} points"

    def __hash__(self):
        if isinstance(self.dice, Dice):
            return hash(self.dice)

        return hash(tuple([d.state for d in self.dice]))

    def __eq__(self, other):
        # Dice to Dice
        if isinstance(other.dice, Dice) and isinstance(self.dice, Dice):
            return other.dice == self.dice
        # [Dice] to [Dice]
        if isinstance(other.dice, Tuple) and isinstance(self.dice, Tuple):
            return [d.state for d in other.dice] == [d.state for d in self.dice]

    def to_json(self):
        return {
            "indexes": [d.index for d in self.dice] if isinstance(self.dice, tuple) else [self.dice.index],
            "points": self.points
        }
    pass
