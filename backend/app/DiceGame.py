from app.dice import Game


class DiceGame:
    def __init__(self, key: str, player_1_name: str, player_2_name: str = None, password: str = None, points_to_win: int = 10000):
        self.game = Game(points_to_win)
        self.password = password
        self.player_1_name = player_1_name
        self.player_2_name = player_2_name
        self.player_1_joined = False
        self.player_2_joined = False
        self.player_1_socket = None
        self.player_2_socket = None
        self.key = key
        pass

    def join_player(self, name, password, websocket):
        if self.password and self.password != password:
            return False

        if self.player_1_name == name:
            self.player_1_joined = True
            self.player_1_socket = websocket
            return True

        if self.player_2_name is None or self.player_2_name == name:
            self.player_2_joined = True
            self.player_2_name = name
            self.player_2_socket = websocket
            return True

        return False

    def player_leave(self, websocket):
        if websocket == self.player_1_socket:
            self.player_1_joined = False
            self.player_1_socket = None
        if websocket == self.player_2_socket:
            self.player_2_joined = False
            self.player_2_socket = None
            pass
        pass

    def has_password(self):
        return bool(self.password)
    pass
