from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.Lobbies import Lobbies
from server.GameHandler import GameHandler
from server.ListHandler import ListHandler
from os.path import dirname, realpath


DIR = dirname(realpath(__file__))
INDEX_HTML = None


app = FastAPI()
app.mount('/static', StaticFiles(directory=f"{DIR}/../frontend/build/static"), name="static")


lobbies = Lobbies()
list_handler = ListHandler(lobbies)
games_handler = {}


@app.get("/")
async def index():
    global INDEX_HTML

    if not INDEX_HTML:
        with open(f"{DIR}/../frontend/build/index.html") as f:
            INDEX_HTML = HTMLResponse(f.read())
            pass
        pass

    return INDEX_HTML
    pass


@app.websocket("/ws/list")
async def websocket_endpoint(websocket: WebSocket):
    await list_handler.manager.connect(websocket)
    try:
        while True:
            await list_handler.on_receive(websocket, await websocket.receive_json())
            pass
        pass
    except WebSocketDisconnect:
        list_handler.manager.disconnect(websocket)
    pass


@app.websocket("/ws/game/{key}")
async def websocket_endpoint(websocket: WebSocket, key: str, password: str = None):
    if key not in lobbies.keys:
        await websocket.accept()
        await websocket.send_json({"event": "game_not_found"})
        await websocket.close()
        return

    if key not in games_handler:
        games_handler[key] = GameHandler(lobbies, key)
        pass

    game_handler = games_handler.get(key)

    await game_handler.on_connect(websocket)
    try:
        while True:
            await game_handler.on_receive(websocket, await websocket.receive_json())
        pass
    except WebSocketDisconnect:
        await game_handler.on_disconnect(websocket)
    pass
