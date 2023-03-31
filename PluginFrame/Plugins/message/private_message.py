import re

from PluginFrame.PluginManager import ModelComponent
from PluginFrame.plugins_conf import registration_directive
from chatgpt.gpt_api import chatbot
from loguru import logger

from cqhttp import SendMsgModel
from cqhttp.api import CQApiConfig
from cqhttp.cq_code import CqReply
from globe import connections
from sk import manager


from cqhttp.request_model import SendPrivateMsgRequest
from utils.text_to_img import to_image


@registration_directive(matching=r'^(?![-.#\[\r\n])([\s\S]*)', message_types=("private",))
class PrivateMessagePlugin(ModelComponent):
    __name__ = 'privateMessage'

    async def start(self, message_parameter):
        message_info = message_parameter.get("message_info")
        sender = message_info.get("sender")
        message_id = message_info.get("message_id")
        logger.info(
            f"收到私人消息：{sender.get('nickname')}({sender.get('user_id')})---->{message_info.get('message')}"
        )
        # 调用GPT-3聊天机器人
        resp = await self.send_message_to_gpt(message_info)
        logger.info(f"回复私人消息：{resp}")
        resp = await to_image(resp)
        resp = CqReply(id=message_id).cq + " " + resp
        await SendPrivateMsgRequest(user_id=sender.get("user_id"), message=resp).send_request(
            CQApiConfig.message.send_private_msg.Api
        )

    async def send_message_to_gpt(self, message_info):
        message = message_info.get("message")
        res = chatbot.ask(message)
        return res

