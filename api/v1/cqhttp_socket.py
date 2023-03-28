from fastapi import APIRouter, WebSocketDisconnect, WebSocket
from message import MessageDispose
from sk import manager

cqhttp = APIRouter()


@cqhttp.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            await MessageDispose(data).dispose(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
