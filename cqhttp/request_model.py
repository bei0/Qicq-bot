from typing import Optional, Union, Any
from cqhttp import bot
from cqhttp.api import CQApiConfig
from pydantic import BaseModel
from loguru import logger


class SendRequest(BaseModel):

    async def send_request(self, api: str):
        try:
            return await bot.call_action(
                api,
                **self.dict()
            )
        except Exception as e:
            logger.error(f"发送请求失败---{e}")

    async def del_message(self, message_id):
        return await bot.call_action(
            CQApiConfig.message.delete_msg.Api,
            {'message_id': message_id}
        )


class SendPrivateMsgRequest(SendRequest):
    user_id: int
    group_id: Optional[int]
    message: Any
    auto_escape: bool = False


class SendPrivateNodeMsgRequest(SendRequest):
    user_id: int
    messages: Any


class SendGroupMsgRequest(SendRequest):
    group_id: int
    message: Any
    auto_escape: bool = False


class SendGroupNodeMsgRequest(SendRequest):
    group_id: int
    messages: Any


class DeleteMsgRequest(SendRequest):
    message_id: int


class GetMessage(SendRequest):
    message_id: int
