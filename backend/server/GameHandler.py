from fastapi import WebSocket
from app.DiceGame import DiceGame
from .ConnectionManager import ConnectionManager
from app.Lobbies import Lobbies
from app.dice.Game import Game
from app.dice.Player import Player


class GameHandler:
    def __init__(self, lobbies: Lobbies, key: str, password: str = None):
        self.manager = ConnectionManager()
        self.lobbies = lobbies
        self.lobby: DiceGame = lobbies.lobbies[key]
        self.game: Game = self.lobby.game
        self.password = password
        pass

    async def on_connect(self, websocket):
        await self.manager.connect(websocket)

    async def on_receive(self, websocket: WebSocket, data):
        if data["event"] == "game_status":
            await websocket.send_json(self.get_game_status(websocket))
        elif data["event"] == "join":
            passwd = self.password if self.password else data.get("password", None)
            if self.lobby.join_player(data["player_name"], passwd, websocket):
                await websocket.send_json({
                    "event": "join_result",
                    "result": True,
                    "you_are": self.get_json_user_type(websocket),
                })
                await self.manager.broadcast_json(callback=self.get_game_status)
            else:
                await websocket.send_json({"event": "join_result", "result": False})
            pass
        elif data["event"] == "roll":
            player = self.get_player_on_turn(websocket)
            if player and self.game.can_roll():
                self.game.roll()
                if not self.game.available_combos():
                    self.game.end_turn()
                await self.manager.broadcast_json(callback=self.get_game_status)
            pass
        elif data["event"] == "confirm_pick":
            player = self.get_player_on_turn(websocket)
            if player and self.game.can_pick():
                self.game.confirm_pick()
                await self.manager.broadcast_json(callback=self.get_game_status)
            pass
        elif data["event"] == "end_turn":
            player = self.get_player_on_turn(websocket)
            if player and self.game.can_roll():
                if self.game.is_winner():
                    await self.manager.broadcast_json({"event": "winner", "winner": self.get_json_user_type(websocket)})
                    self.game.player1.player_state = 0
                    self.game.player2.player_state = 0
                    return

                self.game.end_turn()
                await self.manager.broadcast_json(callback=self.get_game_status)
            pass
        elif data["event"] == "combo_click":
            player = self.get_player_on_turn(websocket)
            if player and self.game.can_pick():
                player.make_combo_by_indexes(data["combo"]["indexes"])
                await self.manager.broadcast_json(callback=self.get_game_status)
            pass
        elif data["event"] == "reset_pick":
            player = self.get_player_on_turn(websocket)
            if player and player.player_state == 2:
                self.game.cancel_pick()
                await self.manager.broadcast_json(callback=self.get_game_status)
            pass
        pass

    async def on_disconnect(self, websocket):
        self.manager.disconnect(websocket)

        if self.is_one_of_players(websocket):
            self.lobby.player_leave(websocket)
            await self.manager.broadcast_json(self.get_game_status(websocket), exclude=[websocket])

        if not (self.lobby.player_1_joined or self.lobby.player_2_joined):
            self.lobbies.close_lobby(self.lobby.key)
            pass
        return websocket

    def get_game_status(self, websocket):
        return {
            "event": "game_status",
            "needs_password": self.lobby.has_password(),
            "you_are": self.get_json_user_type(websocket),
            "player1": {
                "joined": self.lobby.player_1_joined,
                "name": self.lobby.player_1_name,
                "state": self.game.player1.player_state,
                **self.player_to_json(self.game.player1)
            },
            "player2": {
                "joined": self.lobby.player_2_joined,
                "name": self.lobby.player_2_name,
                "state": self.game.player2.player_state,
                **self.player_to_json(self.game.player2)
            },
        }

    def get_players_sockets(self):
        return self.lobby.player_1_socket, self.lobby.player_2_socket

    def is_one_of_players(self, websocket):
        return websocket in self.get_players_sockets()

    def get_player_by_socket(self, websocket):
        if websocket == self.lobby.player_1_socket:
            return self.game.player1
        if websocket == self.lobby.player_2_socket:
            return self.game.player2
        pass

    def get_player_on_turn(self, websocket):
        player = self.get_player_by_socket(websocket)
        return player if player and (player == self.game.on_turn) else None

    def get_json_user_type(self, websocket):
        if self.is_one_of_players(websocket):
            if websocket == self.lobby.player_1_socket:
                return 1
            if websocket == self.lobby.player_2_socket:
                return 2
            pass
        return 0

    @staticmethod
    def player_to_json(player: Player):
        obj = {
            "points": player.points,
            "picked_points": player.picked_points,
            "points_progress": player.points_progress,
            "dice": [d.state for d in player.dice],
            "active_dice": [d.state for d in player.active_dice],
            "picked_dice": [d.state for d in player.picked_dice],
            "stored_dice": [d.state for d in player.stored_dice],
            "combos": [],
        }

        if player.player_state == 2:
            obj["combos"] = [c.to_json() for c in player.get_combos()]

        return obj
    pass
