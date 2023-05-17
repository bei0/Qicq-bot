import aiocqhttp
from aiocqhttp import MessageSegment
from loguru import logger
from PluginFrame.PluginManager import PluginManager
from PluginFrame.plugin_constant import get_black_list, get_manager_qq, code_qq
from PluginFrame.plugins_conf import PluginMatching
from cqhttp import bot


class MessageDispose:

    plugin_parameter = {}

    async def dispose(self, event: aiocqhttp.Event):
        if event.type in ('message', "message_sent"):
            if event.detail_type == "private" and event.type == "message":
                if event.user_id in get_black_list("private"):
                    return
                return await self.__private_message_dispose(event)

            if event.detail_type == "group" and event.type == "message":
                if event.group_id in get_black_list("group") or event.user_id in get_black_list("private"):
                    if event.user_id in get_manager_qq() and "#解禁此群" == event.message:
                        return await self.__group_message_dispose(event)
                await self.__group_message_dispose(event)

        if event.type == "notice":
            if event.get("group_increase"):
                message = MessageSegment.text(f'成员：{event.name}<{event.user_id}>入群了！')
                return await bot.send(event, message)
            if event.get("group_decrease"):
                message = MessageSegment.text(f'成员：{event.name}<{event.user_id}>退群了！')
                return await bot.send(event, message)

    async def __private_message_dispose(self, event):
        re_obj, ma_obj = await PluginMatching.find_matching(event.message, 'private')

        if not ma_obj:
            return

        if plugin := await PluginManager.get_plugin_by_name(ma_obj.plugin_name):
            # 权限认证
            is_per = await self.__permission_authentication(plugin, event)
            if not is_per:
                message = MessageSegment.reply(event.get("message_id")).__add__(
                    MessageSegment.text('您没有权限执行这个操作'))
                return await bot.send(event, message)
                # 传递参数
            self.plugin_parameter["event"] = event
            self.plugin_parameter["bot"] = bot
            self.plugin_parameter["re_obj"] = re_obj
            self.plugin_parameter["ma_obj"] = ma_obj
            # 执行插件开始方法
            logger.info(f"执行插件：{ma_obj.plugin_name}")
            await plugin.start(self.plugin_parameter)
            # queue.put({'func': plugin.start, 'args': (self.plugin_parameter,)})
            # aioscheduler.add_job(func=plugin.start, args=(self.plugin_parameter, ))
        return

    async def __group_message_dispose(self, event):

        re_obj, ma_obj = await PluginMatching.find_matching(event.message, 'group')

        if not ma_obj:
            return

        if plugin := await PluginManager.get_plugin_by_name(ma_obj.plugin_name):
            # 权限认证
            is_per = await self.__permission_authentication(plugin, event)
            if not is_per:
                message = MessageSegment.reply(event.get("message_id")).__add__(
                    MessageSegment.text('您没有权限执行这个操作'))
                return await bot.send(event, message)
            # 传递参数
            self.plugin_parameter["event"] = event
            self.plugin_parameter["re_obj"] = re_obj
            self.plugin_parameter["bot"] = bot
            self.plugin_parameter["ma_obj"] = ma_obj
            # 执行插件开始方法
            logger.info(f"执行插件：{ma_obj.plugin_name}")
            # aioscheduler.add_job(func=plugin.start, args=(self.plugin_parameter, ))
            # queue.put({'func': plugin.start, 'args': (self.plugin_parameter,)})
            await plugin.start(self.plugin_parameter)
        return

    @staticmethod
    async def __permission_authentication(plugin, event):
        if hasattr(plugin, "permissions"):
            if not plugin.permissions:
                return True
            if "all" in plugin.permissions:
                return True
            elif 'code' in plugin.permissions:
                if event.user_id != code_qq:
                    return False
            elif 'admin' in plugin.permissions:
                if event.user_id not in get_manager_qq():
                    return False
            else:
                if event.user_id in plugin.permissions:
                    return True
                else:
                    return False
        return True

