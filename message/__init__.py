
class MessageDispose:

    def __init__(self, message):
        self.message = message

    @staticmethod
    async def dispose(data):
        # 消息处理
        print(data)
        # await manager.send_personal_message(data, connections[0])
        # await manager.broadcast(data)
