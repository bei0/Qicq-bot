import random
import base64
import json
import re
import time
import websockets
import requests
from loguru import logger
from PluginFrame.Plugins import BaseComponentPlugin
from PluginFrame.plugins_conf import registration_directive
from config import Config
from cqhttp.api import CQApiConfig
from cqhttp.cq_code import CqReply, CqNode, CqImage
from cqhttp.request_model import DeleteMsgRequest, SendGroupMsgRequest, SendPrivateMsgRequest

token = None


@registration_directive(matching=r'^#画(.*?)', message_types=("private", 'group'))
class AiImagePlugin(BaseComponentPlugin):
    __name__ = 'AiImagePlugin'

    async def start(self, message_parameter):
        # 调用GPT-3聊天机器人
        message_info = message_parameter.get("message_info")
        re_obj = message_parameter.get("re_obj")
        sender = message_info.get("sender")
        message_id = message_info.get("message_id")
        # 调用GPT-3聊天机器人

        if message_info.get("message_type") == "group":
            logger.info(
                f"收到Ai绘画消息：{re_obj.group(1)}"
            )
            if Config.cqhttp.cqType == "http":
                wait = f"""{CqReply(message_info.get("message_id")).cq} 请稍后..."""
                wait_message = await self.send_group_msg(message_info.get("group_id"), wait)
                avatar_str = self.ai_painting(re_obj.group(1))
                time.sleep(2)
                wait_message = wait_message.get("data")
                await DeleteMsgRequest(message_id=wait_message.get("message_id")).send_request(
                    CQApiConfig.message.delete_msg.Api
                )
            else:
                avatar_str = self.ai_painting(re_obj.group(1))

            if avatar_str == -6:
                await self.send_group_msg(message_info.get("group_id"), "绘画失败，包含非法字符！")
                return

            avatar_str = base64.b64decode(avatar_str)
            image_cq = CqReply(id=message_id).cq + " " + CqImage(
                file="base64://" + base64.b64encode(avatar_str).decode()
            ).cq
            await self.send_group_msg(message_info.get("group_id"), image_cq)

        elif message_info.get("message_type") == "private":
            logger.info(
                f"收到Ai绘画消息：{re_obj.group(1)}"
            )
            if Config.cqhttp.cqType == "http":
                wait = f"""{CqReply(message_info.get("message_id")).cq} 请稍后..."""
                wait_message = await self.send_private_msg(sender.get("user_id"), wait)
                avatar_str = self.ai_painting(re_obj.group(1))
                time.sleep(2)
                wait_message = wait_message.get("data")
                await DeleteMsgRequest(message_id=wait_message.get("message_id")).send_request(
                    CQApiConfig.message.delete_msg.Api
                )
            else:
                avatar_str = self.ai_painting(re_obj.group(1))

            if avatar_str == -6:
                await self.send_private_msg(message_info.get("user_id"), "绘画失败，包含非法字符！")
                return

            avatar_str = base64.b64decode(avatar_str)
            image_cq = CqReply(id=message_id).cq + " " + CqImage(
                file="base64://" + base64.b64encode(avatar_str).decode()
            ).cq
            await self.send_private_msg(sender.get("user_id"), image_cq)

    def get_token(self):
        global token
        if not token:
            res = requests.get(
                "https://flagopen.baai.ac.cn/flagStudio/auth/getToken",
                headers={"Accept": "application/json"}, params={"apikey": Config.baai.apiKey}
            )
            logger.info("获取绘画Token")
            if res.status_code == 200:
                logger.info("获取绘画Token成功---{}".format(res.json().get("data").get("token")))
                token = res.json().get("data").get("token")
                return token
        logger.info("使用已有Token---{}".format(token))
        return token

    def ai_painting(self, prompt):

        token_key = self.get_token()
        url = "https://flagopen.baai.ac.cn/flagStudio/v1/text2img"

        style = ["国画", "写实主义", "虚幻引擎", "黑白插画", "版绘", "电影艺术", "史诗大片", "暗黑", "涂鸦",
                 "漫画场景", "特写", "油画", "水彩画", "素描", "卡通画", "浮世绘", "赛博朋克", "吉卜力", "哑光",
                 "现代中式", "相机", "CG渲染", "动漫", "霓虹游戏", "通用漫画", "Momoko", "MJ风格", "剪纸", "齐白石", "丰子恺"]

        payload = {
            "prompt": f"{prompt}",
            "guidance_scale": 10.0,
            "height": 768,
            "negative_prompts": "",
            "sampler": "ddim",
            "seed": 1024,
            "steps": 50,
            "style": random.choice(style),
            "upsample": 2,
            "width": 512
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "token": f"{token_key}"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        logger.info("开始进行绘画......")
        if response.json()['code'] == 200:

            logger.info("AI绘画完成......")
            return response.json().get('data')
        if response.json()['code'] == -6:
            logger.info("包含非法字符")
            return -6
        return ''
