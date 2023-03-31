import requests
from pydantic import BaseModel
from typing import Optional, List
from config import Config
from cqhttp import SendMsgModel
from globe import connections
from sk import manager


class SendRequest(BaseModel):

    async def send_request(self, api: str, echo='', send_data=None, user_id=None, group_id=None):
        if send_data is None:
            send_data = self.dict()
        if user_id and send_data:
            send_data = {'user_id': user_id, "messages": send_data}
        if group_id and send_data:
            send_data = {'group_id': group_id, "messages": send_data}
        if Config.cqhttp.cqType == 'http':
            res = requests.post(
                url=f'http://{Config.cqhttp.http.host}:{Config.cqhttp.http.port}/{api}',
                json=send_data
            )
            print(send_data)
            print(api)
            print(res.json())
            return res.json()
        if Config.cqhttp.cqType == "ws":
            _ = SendMsgModel(action=api, params=send_data, echo='')
            return await manager.send_personal_message(_.dict(), connections.get_first_connection())
        return


class SendPrivateMsgRequest(SendRequest):
    user_id: int
    group_id: Optional[int]
    message: str
    auto_escape: bool = False


class SendGroupMsgRequest(SendRequest):
    group_id: int
    message: str
    auto_escape: bool = False


class DeleteMsgRequest(SendRequest):
    message_id: int
