import requests
from PluginFrame.Plugins import BaseComponentPlugin
from PluginFrame.plugin_constant import set_choose_data
from PluginFrame.plugins_conf import registration_directive
from aiocqhttp import MessageSegment


@registration_directive(matching=r'#王者语音(| )(.*)', message_types=("private", "group"))
class KingVoicePlugin(BaseComponentPlugin):
    __name__ = 'KingPlugin'
    plu_name = '音频插件'
    desc = "王者荣耀英雄语音包"
    docs = '#王者语音 [英雄名字]'
    permissions = ("admin",)

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        _, king_name = message_parameter.get("re_obj").groups()

        wait_info = await bot.send(event, MessageSegment.reply(event.get("message_id")).__add__(
            MessageSegment.text('请稍后...')
        ))

        message_list, voices = self.get_king(king_name)

        await self.del_wait(wait_info.get("message_id"))

        if message_list == -2:
            await bot.send(event, "王者英雄不存在！")
            return
        elif not message_list:
            await bot.send(event, "接口似乎出现了问题！！")
            return

        message_list.insert(0, MessageSegment.node_custom(
            nickname="北.", user_id=1113855149,
            content=MessageSegment.text("请输入-【序号】选择语音包！")
        ))

        if event.get("message_type") == "group":

            message_info = await self.send(self.send_group_node_msg, group_id=event.get("group_id"))(
                    messages=message_list
                )
            set_choose_data(
                event.user_id, event.message_type, 'king', {"voices": voices, "message_id": message_info.get("message_id")}
            )

        elif event.get("message_type") == "private":

            message_info = await self.send(self.send_private_node_msg, user_id=event.get("user_id"))(
                messages=message_list
            )
            set_choose_data(
                event.user_id, event.message_type, 'king', {"voices": voices, "message_id": message_info.get("message_id")}
            )

    def get_king(self, name):
        _list, lines = [], []
        voices = {}
        try:

            res = requests.get(
                f"https://api.pearktrue.cn/api/game/wzyp.php?msg={name.strip()}", timeout=10
            )
            if res.json().get("code") == -2:
                return -2, []

            king_data = res.json().get("data", []) or []

            for index, king in enumerate(king_data):
                if king.get('lines') not in lines:
                    message = MessageSegment.node_custom(
                        nickname="北.", user_id=1113855149,
                        content=f"""{MessageSegment(type_="reply", data={"text": "序号："+str(index), "qq": 1113855149})}{king.get('lines')}"""
                    )
                    voices[str(index)] = king.get('voice')
                    lines.append(king.get('lines'))
                    _list.append(message)
            return _list, voices
        except:
            return False
