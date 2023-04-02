import requests
from pydantic import BaseModel
from typing import Optional, List, Union, Any
from config import Config
from cqhttp import SendMsgModel
from globe import connections
from sk import manager


class SendRequest(BaseModel):

    async def send_request(self, api: str, echo=''):
        if Config.cqhttp.cqType == 'http':
            res = requests.post(
                url=f'http://{Config.cqhttp.http.host}:{Config.cqhttp.http.port}/{api}',
                json=self.dict()
            )
            return res.json()
        if Config.cqhttp.cqType == "ws":
            _ = SendMsgModel(action=api, params=self.dict(), echo='')
            return await manager.send_personal_message(_.dict(), connections.get_first_connection())
        return


class SendPrivateMsgRequest(SendRequest):
    user_id: int
    group_id: Optional[int]
    message: Union[str, dict, list[dict]]
    auto_escape: bool = False


class SendPrivateNodeMsgRequest(SendRequest):
    user_id: int
    messages: Any


class SendGroupMsgRequest(SendRequest):
    group_id: int
    message: Union[str, dict, list[dict]]
    auto_escape: bool = False


class SendGroupNodeMsgRequest(SendRequest):
    group_id: int
    messages: Any


class DeleteMsgRequest(SendRequest):
    message_id: int
