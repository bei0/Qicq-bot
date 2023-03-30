import json

from globe import connections


class ConnectionManager:

    async def connect(self, ws):
        # 等待连接
        await ws.accept()
        # 存储ws连接对象
        connections.add(ws)

    @staticmethod
    def __disconnect(ws):
        # 关闭时 移除ws对象
        connections.remove(ws)

    @staticmethod
    async def send_personal_message(message: dict, ws):
        # 发送个人消息
        await ws.send_text(json.dumps(message))

    # async def broadcast(self, message: str):
    #     # 广播消息
    #     for connection in connections:
    #         await connection.send_text(message)


manager = ConnectionManager()
