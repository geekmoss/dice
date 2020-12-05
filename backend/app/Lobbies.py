from .DiceGame import DiceGame
from random import choices
from string import ascii_letters


class Lobbies:
    def __init__(self):
        self.keys = set()
        self.lobbies = {}
        pass

    def new_lobby(self, player_1_name, password, points_to_win=10000):
        while True:
            key = "".join(choices(ascii_letters, k=5))
            if key not in self.keys:
                self.keys.add(key)
                break
            pass

        self.lobbies[key] = DiceGame(key, player_1_name, password=password, points_to_win=points_to_win)

        return key

    def close_lobby(self, key):
        if key in self.keys:
            self.keys.remove(key)
            del self.lobbies[key]
    pass
