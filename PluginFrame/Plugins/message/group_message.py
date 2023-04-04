import re

from PluginFrame.PluginManager import ModelComponent
from PluginFrame.plugins_conf import registration_directive
from chatgpt.gpt_api import chatbot
from loguru import logger

from config import Config
from cqhttp import SendMsgModel
from cqhttp.api import CQApiConfig
from cqhttp.cq_code import CqReply
from globe import connections
from sk import manager


from cqhttp.request_model import SendGroupMsgRequest, SendPrivateMsgRequest
from utils.text_to_img import to_image


@registration_directive(matching=r'\[CQ:at,qq=(\w+)] ([\s\S]*)', message_types=("group",))
class GroupMessagePlugin(ModelComponent):
    __name__ = 'groupMessage'

    async def start(self, message_parameter):
        re_obj = message_parameter.get("re_obj")
        message_info = message_parameter.get("message_info")
        message_id = message_info.get("message_id")
        sender = message_info.get("sender")
        if re_obj.group(1) != str(message_info.get("self_id")):
            return

        logger.info(
            f"收到群组({message_info.get('group_id')})消息：{sender.get('nickname')}({sender.get('user_id')})---->{message_info.get('message')}"
        )
        # 调用GPT-3聊天机器人
        resp = await self.send_message_to_gpt(re_obj.group(2))
        logger.info(f"回复私人消息：{resp}")
        if Config.message.text_to_image:
            resp = await to_image(resp)
        resp = CqReply(id=message_id).cq + " " + resp
        await SendGroupMsgRequest(group_id=message_info.get("group_id"), message=resp).send_request(
            CQApiConfig.message.send_group_msg.Api
        )

    async def send_message_to_gpt(self, message):
        res = chatbot.ask(message)
        return res

