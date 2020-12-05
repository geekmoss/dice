from random import randint


class Dice:
    def __init__(self, index=None):
        self.state = 1
        self.index = index
        pass

    def roll(self) -> int:
        self.state = randint(1, 6)
        return self.state

    def __int__(self):
        return self.state

    def __repr__(self):
        return f"{self.state}"

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)
    pass
