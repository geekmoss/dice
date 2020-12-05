from fastapi import WebSocket
from typing import List


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        pass

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        pass

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, exclude: list = None):
        for connection in self.active_connections:
            if exclude and connection in exclude:
                continue

            await connection.send_text(message)
            pass
        pass

    async def broadcast_json(self, data=None, exclude: list = None, callback=None):
        for connection in self.active_connections:
            if exclude and (connection in exclude):
                continue

            if callback and callable(callback):
                data = callback(connection)

            await connection.send_json(data)
        pass
    pass
