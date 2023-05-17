import re
import requests
from PluginFrame.Plugins import BaseComponentPlugin
from PluginFrame.plugins_conf import registration_directive
from aiocqhttp import MessageSegment


@registration_directive(matching=r'^#舔狗', message_types=("private", "group"))
class AnimeWallpapersPlugin(BaseComponentPlugin):
    __name__ = 'AnimeWallpapersPlugin'
    desc = "舔狗日记"
    docs = '#舔狗'
    permissions = ("all",)
    plu_name = '娱乐插件'

    async def start(self, message_parameter):

        message_info = message_parameter.get("event")
        bot = message_parameter.get("bot")
        wait_message = MessageSegment.reply(message_info.get("message_id")).__add__(MessageSegment.text('请稍后...'))
        wait_info = await bot.send(message_info, wait_message)

        data = MessageSegment.reply(message_info.get('message_id')).__add__(
            MessageSegment.text(self.get_tiangou_info())
        )

        await self.del_wait(wait_info.get("message_id"))

        await bot.send(message_info, data)

    @staticmethod
    def get_tiangou_info():
        try:
            resp = requests.get("https://v.api.aa1.cn/api/tiangou/", timeout=10)
            text = re.findall(r"<p>(.*?)</p>", resp.text)
        except:
            text = ["接口似乎出现问题了！！"]
        return text[0]


@registration_directive(matching=r'^#今日热点', message_types=("private", "group"))
class TodayHotSpotPlugin(BaseComponentPlugin):
    __name__ = 'TodayHotSpotPlugin'
    desc = "今日热点"
    docs = '#今日热点'
    permissions = ("admin",)
    plu_name = '娱乐插件'

    async def start(self, message_parameter):
        message_info = message_parameter.get("event")
        bot = message_parameter.get("bot")

        wait_message = MessageSegment.reply(message_info.get("message_id")).__add__(MessageSegment.text('请稍后...'))
        wait_info = await bot.send(message_info, wait_message)
        messages = self.get_girl_url()
        await self.del_wait(wait_info.get("message_id"))

        if message_info.get("message_type") == "group":
            await self.send(self.send_group_node_msg, group_id=message_info.get("group_id"))(
                messages=messages
            )

        elif message_info.get("message_type") == "private":

            await self.send(self.send_private_node_msg, user_id=message_info.get("user_id"))(
                messages=messages
            )

    def get_girl_url(self):
        try:
            resp = requests.get("https://v.api.aa1.cn/api/topbaidu/", timeout=10)
            _dict_list = []
            for _ in resp.json().get("newslist"):
                if not _.get('digest'):
                    continue
                message = MessageSegment.node_custom(
                    nickname="北.", user_id=1113855149,
                    content=f"""{
                    MessageSegment(type_="reply", data={"text": _.get('title'), "qq": 1113855149})
                    } {
                    MessageSegment.text(_.get('digest'))
                    }
                    """
                )
                _dict_list.append(message)
        except:
            _dict_list = [MessageSegment.node_custom(nickname="北.", user_id=1113855149, content=f"接口似乎出现问题了！！")]
        return _dict_list


@registration_directive(matching=r'#权重(\d+|\[CQ:at,qq=(\d+)\])', message_types=("private", "group"))
class WeightPlugin(BaseComponentPlugin):
    __name__ = 'WeightPlugin'
    desc = "查询QQ权重"
    docs = '#权重[QQ号 | @群友]'
    permissions = ("admin",)
    plu_name = '娱乐插件'

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        re_obj = message_parameter.get("re_obj")
        friends_qq, at_qq = re_obj.groups()
        wait_info = await bot.send(event, MessageSegment.reply(event.get("message_id")).__add__(
            MessageSegment.text('请稍后...')
        ))

        if at_qq:
            message = self.get_weight(qq=at_qq)
        else:
            message = self.get_weight(qq=friends_qq)

        await self.del_wait(wait_info.get("message_id"))

        await bot.send(event, message)

        return

    def get_weight(self, qq):
        try:
            res = requests.get(f"http://tfapi.top/API/qqqz.php?type=json&qq={qq}")
            qz = res.json().get("qz")
            return F"Qq:{qq}, 权重：{qz}"
        except:
            return "接口似乎出现了问题！！"
