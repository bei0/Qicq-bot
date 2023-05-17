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
from aiocqhttp import MessageSegment

token = None


@registration_directive(matching=r'^#画(|.*?) (.*?)', message_types=("private", 'group'))
class AiImagePlugin(BaseComponentPlugin):
    __name__ = 'AiImagePlugin'
    desc = "Ai绘画"
    docs = "#画[绘画风格] [描述语]"
    plu_group = "AI绘画插件"
    permissions = ("admin",)
    plu_name = '图片插件'

    async def start(self, message_parameter):
        # 调用GPT-3聊天机器人
        re_obj = message_parameter.get("re_obj")
        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        sender = event.sender
        message_id =event.message_id
        # 调用GPT-3聊天机器人

        style, description = re_obj.groups()
        styles = ["国画", "写实主义", "相机", "黑白插画", "版绘", "电影艺术", "史诗大片", "暗黑", "涂鸦",
                  "漫画场景", "特写", "油画", "水彩画", "素描", "卡通画", "动漫", "Momoko", "通用漫画"]
        if style.strip() not in styles:
            style = 'Momoko'

        logger.info(
            f"收到Ai{style}风格绘画消息：{description}"
        )

        wait_info = await bot.send(event, MessageSegment.reply(event.get("message_id")).__add__(
            MessageSegment.text(f'绘画风格：{style}, 请稍后...')
        ))
        status, avatar_str = self.ai_painting(style, description)
        await self.del_wait(wait_info.get("message_id"))

        if not status:
            await bot.send(event, avatar_str)
            return

        avatar_str = base64.b64decode(avatar_str)

        image_cq = MessageSegment.reply(id_=message_id).__add__(
            MessageSegment.image(
                file="base64://" + base64.b64encode(avatar_str).decode()
            )
        )
        await bot.send(event, image_cq)

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

    def ai_painting(self, style, description):

        token_key = self.get_token()
        url = "https://flagopen.baai.ac.cn/flagStudio/v1/text2img"
        payload = {
            "prompt": f"{description.strip()}",
            "guidance_scale": 20,
            "height": 768,
            "negative_prompts": "",
            "sampler": "ddim",
            # "seed": 0xfffffffffffffff,
            "steps": 50,
            "style": style.strip(),
            "upsample": 1,
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
            return True, response.json().get('data')
        if response.json()['code'] != 200:
            return False, response.json()['data']
        return ''
