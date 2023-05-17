import json
import os
import random
import time

from aiocqhttp import MessageSegment

from PluginFrame.Plugins import BaseComponentPlugin
from PluginFrame.plugin_constant import set_choose_data, get_choose_data, del_choose_data
from PluginFrame.plugins_conf import registration_directive

tor_path = os.path.dirname(os.path.abspath(__file__))


@registration_directive(matching=r'^#抽([1-3])张?(塔罗牌|大阿(尔)?卡纳|小阿(尔)?卡纳)$', message_types=("private", "group"))
class TarotPlugin(BaseComponentPlugin):
    __name__ = 'TarotPlugin'
    desc = "塔罗牌"
    docs = '#抽[1-3]张[塔罗牌|大阿卡纳|小阿卡纳]'
    permissions = ("all",)
    plu_name = '塔罗牌插件'

    # 插件内
    bed = "https://gitcode.net/shudorcl/zbp-tarot/-/raw/master/"
    tarots_data = {}
    reasons = ["您抽到的是~", "锵锵锵，塔罗牌的预言是~", "诶，让我看看您抽到了~"]
    position = ["『正位』", "『逆位』"]
    reverse = ["", "Reverse/"]

    async def start(self, message_parameter):

        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        re_obj = message_parameter.get("re_obj")
        match, card_type, _, _ = re_obj.groups()

        start = 22 if "小" in card_type else 0
        length = 55 if "小" in card_type else 22

        if not self.tarots_data:
            self.load_tarots()
        wait_info = await bot.send(event, MessageSegment.reply(event.get("message_id")).__add__(
            MessageSegment.text(random.choice(self.reasons))
        ))

        card_list_infos = []
        exclude_num = []
        for i in range(int(match)):
            num = random.randint(start, length)
            # 去掉抽取的重复牌
            if num in exclude_num:
                while True:
                    num = random.randint(start, length)
                    exclude_num.append(num)
                    if num not in exclude_num:
                        break
            exclude_num.append(num)

            card = self.tarots_data.get(str(num))
            p = random.randint(0, 1)
            name = card.get("name")
            info = card.get("info")
            reverse = self.reverse[p]
            description = info.get("reverseDescription") if reverse else info.get("description")
            img_url = self.bed + reverse + info.get("imgUrl")

            text = f"牌名：\n{name}{self.position[p]}\n其释义为：\n{description}"
            message = MessageSegment.node_custom(
                nickname="北.", user_id=1113855149,
                content=f"""{MessageSegment.image(file=img_url)}\n{text}"""
            )
            card_list_infos.append(message)

        await self.del_wait(wait_info.get("message_id"))

        if event.message_type == "group":
            message_info = await self.send(self.send_group_node_msg, group_id=event.get("group_id"))(
                    messages=card_list_infos
                )
        elif event.get("message_type") == "private":
            message_info = await self.send(self.send_private_node_msg, user_id=event.get("user_id"))(
                messages=card_list_infos
            )

    def load_tarots(self):
        with open(os.path.join(tor_path, "data/tarots.json"), "r", encoding="utf-8") as tarots:
            self.tarots_data = json.loads(tarots.read())


@registration_directive(matching=r'^#(塔罗|大阿(尔)?卡纳|小阿(尔)?卡纳|混合)牌阵?(.*)', message_types=("private", "group"))
class TarotFormationPlugin(BaseComponentPlugin):
    __name__ = 'TarotFormationPlugin'
    desc = "塔罗牌阵"
    docs = '#[塔罗|大阿卡纳|小阿卡纳|混合]牌阵[圣三角|时间之流|四要素|五牌阵|吉普赛十字|马蹄|六芒星]'
    permissions = ("all",)
    plu_name = '塔罗牌插件'

    # 插件内
    bed = "https://gitcode.net/shudorcl/zbp-tarot/-/raw/master/"
    tarots_data = {}
    formation = {}
    position = ["『正位』", "『逆位』"]
    reverse = ["", "Reverse/"]

    async def start(self, message_parameter):

        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        re_obj = message_parameter.get("re_obj")
        card_type, _, _, formation = re_obj.groups()

        if not self.tarots_data:
            self.load_tarots()
        if not self.formation:
            self.load_formation()

        tion_info = self.formation.get(formation)
        if not tion_info:
            await bot.send(event, f"没有找到{formation}噢~\n现有牌阵列表:\n{','.join(self.formation.keys())}")
            return

        start, length = 0, 22
        if "小" in card_type:
            start, length = 22, 55
        elif "混合" in card_type:
            start, length = 0, 77

        match = tion_info.get("cards_num")
        wait_info = await bot.send(event, MessageSegment.reply(event.get("message_id")).__add__(
            MessageSegment.text("少女祈祷中...")
        ))

        card_list_infos = []
        exclude_num = []
        for i in range(int(match)):
            num = random.randint(start, length)
            # 去掉抽取的重复牌
            if num in exclude_num:
                while True:
                    num = random.randint(start, length)
                    exclude_num.append(num)
                    if num not in exclude_num:
                        break
            exclude_num.append(num)

            card = self.tarots_data.get(str(num))
            p = random.randint(0, 1)
            name = card.get("name")
            info = card.get("info")
            reverse = self.reverse[p]
            description = info.get("reverseDescription") if reverse else info.get("description")
            img_url = self.bed + reverse + info.get("imgUrl")

            text = f"牌名：\n{name}{self.position[p]}\n代表:{tion_info['represent'][0][i]}\n其释义为：\n{description}"
            message = MessageSegment.node_custom(
                nickname="北.", user_id=1113855149,
                content=f"""{MessageSegment.image(file=img_url)}\n{text}"""
            )
            card_list_infos.append(message)

        await self.del_wait(wait_info.get("message_id"))

        if event.message_type == "group":
            message_info = await self.send(self.send_group_node_msg, group_id=event.get("group_id"))(
                    messages=card_list_infos
                )
        elif event.get("message_type") == "private":
            message_info = await self.send(self.send_private_node_msg, user_id=event.get("user_id"))(
                messages=card_list_infos
            )

    def load_tarots(self):
        with open(os.path.join(tor_path, "data/tarots.json"), "r", encoding="utf-8") as tarots:
            self.tarots_data = json.loads(tarots.read())

    def load_formation(self):
        with open(os.path.join(tor_path, "data/formation.json"), "r", encoding="utf-8") as tarots:
            self.formation = json.loads(tarots.read())
