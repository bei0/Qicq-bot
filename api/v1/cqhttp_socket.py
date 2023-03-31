import time

from fastapi import APIRouter, WebSocketDisconnect, WebSocket

from globe import connections
from message import MessageDispose
from sk import manager

cqhttp = APIRouter()


@cqhttp.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    if len(connections.connections) > 1:
        raise WebSocketDisconnect(4001, "Only one connection is allowed")

    try:
        while True:
            data = await websocket.receive_json()
            message_dispose = MessageDispose()
            await message_dispose.dispose(data)
    except Exception as e:
        print(e)
        connections.remove(websocket)
        print("Client disconnected")


@cqhttp.post("/callback")
async def websocket_endpoint(body: dict):
    message_dispose = MessageDispose()
    await message_dispose.dispose(body)
    return {
        "status": "ok",
        "retcode": 0,
        'data': {},
    }
