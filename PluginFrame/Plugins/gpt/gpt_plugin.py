# from PluginFrame.Plugins import BaseComponentPlugin
# from PluginFrame.plugins_conf import registration_directive
# from loguru import logger
# from constants import config
# from platforms.onebot_bot import transform_message_chain
# from universal import handle_message
# from middlewares.ratelimit import manager as ratelimit_manager
#
#
# @registration_directive(matching=r'^\.设置 (\w+) (\S+) 额度为 (\d+)条/小时', message_types=("private", "group"))
# class SetUpQuotasPlugin(BaseComponentPlugin):
#     __name__ = 'SetUpQuotasPlugin'
#     plu_name = 'ChatGpt插件'
#     desc = "设置每小时GPT额度"
#     docs = ".设置 [群组/好友] [群号/QQ号] 额度为 [99]条/小时"
#     permissions = ("admin",)
#
#     async def start(self, message_parameter):
#
#         event = message_parameter.get("event")
#         # 获取正则对象
#         re_obj = message_parameter.get("re_obj")
#         # 获取机器人对象
#         bot = message_parameter.get("bot")
#         msg_type, msg_id, rate = re_obj.groups()
#
#         if msg_type not in ["群组", "好友"]:
#             return await bot.send(event, "类型异常，仅支持设定【群组】或【好友】的额度")
#         if msg_id != '默认' and not msg_id.isdecimal():
#             return await bot.send(event, "目标异常，仅支持设定【默认】或【指定 QQ（群）号】的额度")
#         ratelimit_manager.update(msg_type, msg_id, int(rate))
#         return await bot.send(event, "额度更新成功！")
#
#
# @registration_directive(matching=r'\[CQ:at,qq=(\w+)] ([\s\S]*)', message_types=("group",))
# class GroupMessagePlugin(BaseComponentPlugin):
#     __name__ = 'groupMessage'
#     desc = "群聊GPT回答机器人"
#     docs = "@机器人QQ [提问的问题]【无绘画接口】"
#     plu_name = 'ChatGpt插件'
#
#     async def start(self, message_parameter):
#         re_obj = message_parameter.get("re_obj")
#         event = message_parameter.get("event")
#         bot = message_parameter.get("bot")
#         if re_obj.group(1) != str(event.self_id):
#             return
#         # 调用GPT-3聊天机器人
#         chain = transform_message_chain(event.message)
#         await handle_message(
#             self.response(event, True, bot),
#             f"group-{event.group_id}",
#             event.message,
#             chain,
#             is_manager=event.user_id == config.onebot.manager_qq,
#             nickname=event.sender.get("nickname", "群友")
#         )
#
#
# @registration_directive(matching=r'^(?![-.#\[\r\n])([\s\S]*)', message_types=("private",))
# class PrivateMessagePlugin(BaseComponentPlugin):
#     __name__ = 'privateMessage'
#     desc = "私聊GPT回答机器人"
#     docs = "提问非 -.# 开头的问题 [GPT绘画指令：画【描述语】]"
#     plu_name = 'ChatGpt插件'
#
#     async def start(self, message_parameter):
#         event = message_parameter.get("event")
#         bot = message_parameter.get("bot")
#         sender = event.sender
#         logger.info(
#             f"收到私人消息：{sender.get('nickname')}({sender.get('user_id')})---->{event.message}"
#         )
#         # 调用GPT-3聊天机器人
#         chain = transform_message_chain(event.message)
#         await handle_message(
#             self.response(event, False, bot),
#             f"friend-{event.user_id}",
#             event.message,
#             chain,
#             is_manager=event.user_id == config.onebot.manager_qq,
#             nickname=event.sender.get("nickname", "好友")
#         )
