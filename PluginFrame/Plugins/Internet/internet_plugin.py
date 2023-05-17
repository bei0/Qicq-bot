import requests
from loguru import logger
from PluginFrame.Plugins import BaseComponentPlugin
from PluginFrame.plugins_conf import registration_directive
from aiocqhttp import MessageSegment


@registration_directive(matching=r'^#(ping|Ping) (.*)', message_types=("private", "group"))
class PingHostPlugin(BaseComponentPlugin):
    __name__ = 'PingHostPlugin'
    desc = "Ping域名"
    docs = '#Ping / #ping [baidu.com]'
    permissions = ("admin",)
    plu_name = '网络插件'

    async def start(self, message_parameter):
        message_info = message_parameter.get("event")
        sender = message_info.sender
        re_obj = message_parameter.get("re_obj")
        host = re_obj.group(2)
        if message_info.get("message_type") == "group":
            logger.info(
                f"收到群组({message_info.get('group_id')})消息：{sender.get('nickname')}({sender.get('user_id')})---->{message_info.get('message')}"
            )

            wait_info = await self.send_wait(self.send_group_msg, group_id=message_info.get("group_id"))(
                message_info.get("message_id"), "请稍后..."
            )
            status, data = self.get_girl_url(host)
            await self.del_wait(wait_info.get("message_id"))
            data = f"{MessageSegment.reply(message_info.get('message_id'))} {data}"
            await self.send_group_msg(message_info.get("group_id"), str(data))

        elif message_info.get("message_type") == "private":
            logger.info(
                f"收到私人消息：{sender.get('nickname')}({sender.get('user_id')})---->{message_info.get('message')}"
            )

            wait_info = await self.send_wait(self.send_private_msg, user_id=message_info.get("user_id"))(
                message_info.get("message_id"), "请稍后..."
            )
            status, data = self.get_girl_url(host)

            await self.del_wait(wait_info.get("message_id"))
            await self.send_private_msg(sender.get("user_id"), data)
        return ''

    @staticmethod
    def get_girl_url(url):
        resp = requests.get(f"https://v.api.aa1.cn/api/api-ping/ping.php?url={url}")
        try:
            resp = resp.json()
            data = f"""
            Ping {url} 的结果为：
             域名：{resp.get("host")}
             IP：{resp.get("ip")}
             最小延迟：{resp.get("ping_time_min")}
             最大延迟：{resp.get("ping_time_max")}
             服务器运营部：{resp.get("location")}
             服务器归属地：{resp.get("node")}
            """
            status = 0
        except Exception as e:
            print(e)
            data = resp.text
            status = 1
        return status, data