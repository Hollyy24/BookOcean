from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set


router = APIRouter()


user_connections: Dict[str, Set[WebSocket]] = {}


@router.websocket("/ws/{temp_token}")
async def websocket_online(websocket: WebSocket, temp_token: str):
    await websocket.accept()
    if temp_token not in user_connections:
        user_connections[temp_token] = set()
        user_connections[temp_token].add(websocket)

        await broadcast_online_count()

        try:
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            user_connections[temp_token].remove(websocket)
            if not user_connections[temp_token]:
                del user_connections[temp_token]
            await broadcast_online_count()


async def broadcast_online_count():
    count = len(user_connections)
    for ws_set in user_connections.values():
        for ws in ws_set:
            try:
                await ws.send_json({"count": count})
            except:
                pass
