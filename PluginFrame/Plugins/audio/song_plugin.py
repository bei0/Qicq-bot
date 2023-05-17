import json
import re
import requests
from PluginFrame.Plugins import BaseComponentPlugin
from PluginFrame.plugin_constant import set_choose_data
from PluginFrame.plugins_conf import registration_directive
from aiocqhttp import MessageSegment


@registration_directive(matching=r'#点歌(.*|) (.*)', message_types=("private", "group"))
class MusicPlugin(BaseComponentPlugin):
    __name__ = 'MusicPlugin'
    desc = "点歌系统（网易云）"
    plu_name = '音频插件'
    docs = '#点歌[网易云|酷狗] [歌曲名称]'
    permissions = ("admin",)

    async def start(self, message_parameter):

        types = {
            "网易云": "netease",
            "酷狗": "kugou",
            "QQ": "QQ",
            "qq": "QQ",
        }

        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        music_type, music_name = message_parameter.get("re_obj").groups()

        music_type = types.get(music_type, '') or "netease"

        wait_info = await bot.send(event, MessageSegment.reply(event.get("message_id")).__add__(
            MessageSegment.text('请稍后...')
        ))

        if music_type == "netease":
            r_id_info, r_ids = self.get_netease_music(music_name)
        elif music_type == "QQ":
            r_id_info, r_ids = await self.get_qq_music(music_name)
        else:
            r_id_info, r_ids = await self.get_kugou_music(music_name)

        await self.del_wait(wait_info.get("message_id"))

        if not r_id_info:
            await bot.send(event, "接口似乎出现了问题！！")
            return

        r_id_info.insert(0, MessageSegment.node_custom(
            nickname="北.", user_id=1113855149,
            content=MessageSegment.text("请输入-【序号】选择歌曲！")
        ))

        if event.get("message_type") == "group":

            message_info = await self.send(self.send_group_node_msg, group_id=event.get("group_id"))(
                    messages=r_id_info
                )
            set_choose_data(
                event.user_id, event.message_type, 'mus', {
                    "r_ids": r_ids, "message_id": message_info.get("message_id"), "type": music_type,
                    "music_name": music_name
                }
            )

        elif event.get("message_type") == "private":

            message_info = await self.send(self.send_private_node_msg, user_id=event.get("user_id"))(
                messages=r_id_info
            )
            set_choose_data(
                event.user_id, event.message_type, 'mus', {
                    "r_ids": r_ids, "message_id": message_info.get("message_id"), "type": music_type,
                    "music_name": music_name
                }
            )

    def get_netease_music(self, name):
        _list = []
        r_ids = {}

        try:
            res = requests.get(
                f"https://api.pearktrue.cn/api/music/search.php?name={name}&type=netease&page=1", timeout=10
            )
            music_data = res.json().get("data", []) or []
            for index, music in enumerate(music_data):
                id = re.fullmatch("http://music.163.com/song/media/outer/url\?id=(.*).mp3", music.get('playurl'))
                if not id:
                    continue
                r_id = id.group(1)
                r_ids[str(index+1)] = r_id
                message = MessageSegment.node_custom(
                    nickname="北.", user_id=1113855149,
                    content=f"""{MessageSegment(type_="reply", data={"text": "序号："+str(index+1), "qq": 1113855149})}歌名：《{music.get('title')}》\n演唱：{music.get('author')}"""
                )
                _list.append(message)
            return _list, r_ids
        except:
            return False, False

    async def get_kugou_music(self, name):
        _list = []
        r_ids = {}

        try:
            res = requests.get(
                f"https://v.api.aa1.cn/api/kugou/?msg={name}", timeout=10
            )
            a = json.loads(res.text, strict=False)
            data = a.get("data")
            data_1 = data.split('\n')
            for data_info in data_1:
                data_2 = data_info.split('：')
                if data_2[0]:
                    r_ids[str(data_2[0])] = data_2[0]
                    message = MessageSegment.node_custom(
                        nickname="北.", user_id=1113855149,
                        content=f"""{MessageSegment(type_="reply", data={"text": "序号："+str(data_2[0]), "qq": 1113855149})}《{data_2[1]}》"""
                    )
                    _list.append(message)
            return _list, r_ids
        except:
            return False, False

    async def get_qq_music(self, name):
        _list = []
        r_ids = {}

        try:
            res = requests.get(
                f"https://api.xingzhige.com/API/QQmusicVIP_new/?msg={name}&limit=30", timeout=10
            )

            data_json = res.json()
            if data_json.get("code") == 0:
                music_data = data_json.get("data")
                for index, data_info in enumerate(music_data):
                    r_ids[str(index+1)] = {"id": data_info.get("songid"), "mid": data_info.get("mid")}
                    message = MessageSegment.node_custom(
                        nickname="北.", user_id=1113855149,
                        content=f"""{MessageSegment(type_="reply", data={"text": "序号：" + str(index+1), "qq": 1113855149})}歌曲：《{data_info.get("song")}》\n演唱：{" ".join(data_info.get("singers"))}"""
                    )
                    _list.append(message)

                return _list, r_ids
            else:
                return False, data_json.get("msg")
        except:
            return False, "查询歌曲失败！"
