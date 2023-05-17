import os
import sys

import requests
from aiocqhttp import MessageSegment
from loguru import logger

from PluginFrame.PluginManager import PluginManager
from PluginFrame.Plugins import BaseComponentPlugin
from PluginFrame.plugin_constant import del_choose_data, get_choose_data, reset_plugins
from PluginFrame.plugins_conf import registration_directive
from config import Config


# @registration_directive(matching=r'#重启', message_types=("private", "group"))
# class RebootPlugin(BaseComponentPlugin):
#     __name__ = 'RebootPlugin'
#     desc = ""
#     docs = ""
#     permissions = ("admin", )
#     plu_name = ''
#
#     async def start(self, message_parameter):
#         event = message_parameter.get("event")
#         bot = message_parameter.get("bot")
#
#         constants.config = config.load_config()
#         config.scan_presets()
#         await bot.send(event, "配置文件重新载入完毕！")
#         await bot.send(event, "重新登录账号中，详情请看控制台日志……")
#         constants.botManager = BotManager(config)
#         await botManager.login()
#         await bot.send(event, "登录结束")


@registration_directive(matching=r'^\[CQ:reply,id=(-\d+|\d+)\](\[CQ:at,qq=(\d+)\]|)(| )撤回',
                        message_types=("private", "group"))
class MessageWithdrawPlugin(BaseComponentPlugin):
    __name__ = 'MessageWithdrawPlugin'
    desc = "消息撤回"
    docs = ''
    permissions = ("all",)
    plu_name = ''

    async def start(self, message_parameter):

        message_id, _, qq, _ = message_parameter.get("re_obj").groups()
        try:
            await self.del_wait(message_id)
        except Exception as e:
            logger.debug(f"消息撤回失败---{e}")


@registration_directive(matching=r'-(| )(\d+)', message_types=("private", "group"))
class ChoosePlugin(BaseComponentPlugin):
    __name__ = 'ChoosePlugin'
    desc = ""
    docs = ''
    plu_name = ''
    permissions = ("all",)

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        _, choose_id = message_parameter.get("re_obj").groups()
        _data = get_choose_data(event.user_id, event.message_type)
        if 'mus' in _data:
            await self.mus_send(event, choose_id, _data, bot)
        elif 'king' in _data:
            await self.king_send(event, choose_id, _data, bot)
        return

    async def mus_send(self, event, choose_id, _data, bot):
        mus = _data.get("mus", {}) or {}
        if not mus:
            return
        r_ids = mus.get('r_ids')
        if not r_ids:
            return
        if choose_id not in r_ids.keys():
            await bot.send(event, "歌曲序号不正确！重新选择")
            return False

        id_ = r_ids.get(choose_id)
        mus_type = mus.get("type")
        music_name = mus.get("music_name")
        if mus_type == "netease":
            message = MessageSegment.music(type_='163', id_=id_)
        elif mus_type == "kugou":
            res = requests.get(f"https://v.api.aa1.cn/api/kugou/?msg={music_name}&type={id_}")
            res_json = res.json()
            if res_json.get("PlayLink"):
                # message = MessageSegment.music_custom(
                #     url="http://www.kugou.com/song",
                #     audio_url=res_json.get("PlayLink"),
                #     title=res_json.get("SongTitle"),
                #     image_url=res_json.get("img"),
                #
                # )
                message = MessageSegment.record(file=res_json.get("PlayLink"))
            else:
                message = MessageSegment.text(res_json.get("msg"))

        elif mus_type == "QQ":
            message = MessageSegment.music(type_='qq', id_=id_.get("id"))
        else:
            return
        await self.del_wait(mus.get("message_id", ''))
        await bot.send(event, message)
        del_choose_data(event.user_id)
        return message

    async def king_send(self, event, choose_id, _data, bot):
        mus = _data.get("king", {}) or {}
        if not mus:
            return
        voices = mus.get('voices')
        if not voices:
            return
        try:
            voice = voices.get(str(choose_id).strip())
        except:
            await bot.send(event, "歌曲序号不正确！重新选择")
            return False
        message = MessageSegment.record(file=voice)
        await self.del_wait(mus.get("message_id", ''))
        await bot.send(event, message)
        del_choose_data(event.user_id)
        return message


@registration_directive(matching=r'#重新加载插件', message_types=("private", "group"))
class RePlugin(BaseComponentPlugin):
    __name__ = 'RePlugin'
    desc = ""
    docs = ""
    permissions = ("code",)
    plu_name = ''

    async def start(self, message_parameter):

        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        reset_plugins()
        PluginManager.PluginPath = 'Plugins'
        PluginManager.reload_the_plugin()
        await bot.send(event, "重新加载插件成功！")
