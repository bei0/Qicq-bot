
from PluginFrame.PluginManager import ModelComponent
from PluginFrame.plugins_conf import registration_directive
from chatgpt.gpt_api import chatbot
from loguru import logger

from cqhttp import SendMsgModel
from cqhttp.api import CQApiConfig
from globe import connections
from sk import manager


from cqhttp.request_model import SendGroupMsgRequest
from utils.text_to_img import to_image


@registration_directive(matching=r'\[CQ:(\w+),qq=(\w+)] (.*)', message_types=("group",))
class GroupMessagePlugin(ModelComponent):
    __name__ = 'groupMessage'

    async def start(self, message_parameter):
        re_obj = message_parameter.get("re_obj")
        message_info = message_parameter.get("message_info")
        sender = message_info.get("sender")
        if re_obj.group(1) != "at" or re_obj.group(2) != str(message_info.get("self_id")):
            return

        logger.info(
            f"收到群组({message_info.get('group_id')})消息：{sender.get('nickname')}({sender.get('user_id')})---->{message_info.get('message')}"
        )
        # 调用GPT-3聊天机器人
        resp = await self.send_message_to_gpt(re_obj.group(3))
        logger.info(f"回复私人消息：{resp}")
        resp = await to_image(resp)
        send_data = SendMsgModel(
            action=CQApiConfig.message.send_group_msg.Api,
            params=SendGroupMsgRequest(group_id=message_info.get("group_id"), message=resp).dict(),
            echo="发送群组消息成功"
        ).dict()
        await manager.send_personal_message(send_data, connections.get_first_connection())

    async def send_message_to_gpt(self, message):
        res = chatbot.ask(message)
        return res
