import asyncio
import base64
import json
import re
import time
import websockets
import requests
from loguru import logger

from PluginFrame.PluginManager import ModelComponent
from PluginFrame.Plugins import BaseComponentPlugin
from PluginFrame.plugins_conf import registration_directive
from config import Config
from cqhttp.api import CQApiConfig
from cqhttp.cq_code import CqReply, CqNode, CqImage
from cqhttp.request_model import DeleteMsgRequest, SendGroupMsgRequest, SendPrivateMsgRequest


@registration_directive(matching=r'^#画(.*?)', message_types=("private",))
class AiImagePlugin(BaseComponentPlugin):
    __name__ = 'AiImagePlugin'

    async def start(self, message_parameter):
        # 调用GPT-3聊天机器人
        message_info = message_parameter.get("message_info")
        re_obj = message_parameter.get("re_obj")
        sender = message_info.get("sender")
        # 调用GPT-3聊天机器人

        if message_info.get("message_type") == "group":
            logger.info(
                f"收到Ai会话消息：{re_obj.group(1)}"
            )
            data_ai = {}
            if Config.cqhttp.cqType == "http":
                wait = f"""{CqReply(message_info.get("message_id")).cq} 请稍后..."""
                wait_message = await self.send_group_msg(message_info.get("group_id"), wait)
                data_ai = await self.connect(self.translation(re_obj.group(1)))
                wait_message = wait_message.get("data")
                await DeleteMsgRequest(message_id=wait_message.get("message_id")).send_request(
                    CQApiConfig.message.delete_msg.Api
                )
            else:
                data_ai = await self.connect(self.translation(re_obj.group(1)))

            _dict_list = []
            for _ in data_ai.get("output", {}).get("data")[0]:
                avatar_str = _.split(',', 1)[1]
                avatar_str = base64.b64decode(avatar_str)
                _dict = CqNode(name="北.", uin=1113855149,
                               content=f'{CqImage(file="base64://" + base64.b64encode(avatar_str).decode()).cq}').json
                _dict_list.append(_dict)
            await self.send_group_node_msg(message_info.get("group_id"), _dict_list)

        elif message_info.get("message_type") == "private":
            logger.info(
                f"收到私人消息：{sender.get('nickname')}({sender.get('user_id')})---->{message_info.get('message')}"
            )
            if Config.cqhttp.cqType == "http":
                wait = f"""{CqReply(message_info.get("message_id")).cq} 请稍后..."""
                wait_message = await self.send_private_msg(sender.get("user_id"), wait)
                data_ai = await self.connect(self.translation(re_obj.group(1)))
                wait_message = wait_message.get("data")
                await DeleteMsgRequest(message_id=wait_message.get("message_id")).send_request(
                    CQApiConfig.message.delete_msg.Api
                )
            else:
                data_ai = await self.connect(self.translation(re_obj.group(1)))
            _dict_list = []
            for _ in data_ai.get("output", {}).get("data")[0]:
                avatar_str = _.replace('data:image/jpeg;base64,', '')
                avatar_str = base64.b64decode(avatar_str)
                _dict = CqNode(name="北.", uin=1113855149,
                               content=f'{CqImage(file="base64://" + base64.b64encode(avatar_str).decode()).cq}').json
                _dict_list.append(_dict)
            await self.send_private_node_msg(sender.get("user_id"), _dict_list)

    async def connect(self, image_description):
        uri = 'wss://stabilityai-stable-diffusion-1.hf.space/queue/join'
        try:
            async with websockets.connect(uri,) as websocket_obj:
                while True:
                    greeting = await websocket_obj.recv()
                    data = json.loads(greeting)
                    if data.get("msg") == 'process_completed':
                        logger.info(f"画图成功！！！！")
                        return data
                    await websocket_obj.send(json.dumps({"session_hash": "7am7qz0vo6o", "fn_index": 3}))
                    await websocket_obj.send(json.dumps(
                        {"fn_index": 3, "data": [image_description], "session_hash": "7am7qz0vo6o"}
                    ))

        except:
            logger.error(f"画图失败！！！！")
            return {}

    def translation(self, text):
        try:
            url = f"https://v.api.aa1.cn/api/api-fanyi-yd/index.php?msg={text}&type=3"
            response = requests.get(url)
            data = response.json().get('text')
        except:
            data = text
        return data


# asyncio.get_event_loop().run_until_complete(AnimeWallpapersPlugin().start())
