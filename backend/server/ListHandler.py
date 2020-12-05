from fastapi import WebSocket

from app.DiceGame import DiceGame
from .ConnectionManager import ConnectionManager
from app.Lobbies import Lobbies


class ListHandler:
    def __init__(self, lobbies: Lobbies):
        self.manager = ConnectionManager()
        self.lobbies = lobbies
        pass

    def get_lobbies_json(self):
        l = self.lobbies.lobbies
        return [{
            "key": key,
            "player_1_name": l[key].player_1_name,
            "player_2_name": l[key].player_2_name,
            "player_1_points": l[key].game.player1.points,
            "player_2_points": l[key].game.player2.points,
            "points_to_win": l[key].game.points_to_win,
            "has_password": l[key].has_password(),
        } for key in self.lobbies.keys]
        pass

    async def on_receive(self, websocket: WebSocket, data):
        if data["event"] == "list":
            await websocket.send_json({"event": "list", "lobbies": self.get_lobbies_json()})
        elif data["event"] == "new_room":
            key = self.lobbies.new_lobby(
                data["room"]["player_name"],
                data["room"].get("password", None),
                data["room"]["points"]
            )
            await websocket.send_json({
                "event": "new_room",
                "room": {
                    "key": key,
                    "password": data["room"].get("password", "")
                }
            })
            await self.manager.broadcast_json({"event": "list", "lobbies": self.get_lobbies_json()})
        pass
    pass
