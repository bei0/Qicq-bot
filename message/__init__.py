from loguru import logger

from PluginFrame.PluginManager import PluginManager
from PluginFrame.plugins_conf import PluginMatching


class MessageDispose:

    plugin_parameter = {}

    async def dispose(self, message):

        if "echo" in message.keys():
            logger.info(f"收到消息上报：-{message.get('echo')}")
            return
        # 消息处理
        if (post_type := message['post_type']) in ('message', "message_sent"):
            await self.__message_report_data_processing(post_type, message)

    # 消息上报处理逻辑
    async def __message_report_data_processing(self, post_type, message):
        # 消息分类处理
        if message['message_type'] == "private" and post_type == "message":
            await self.__private_message_dispose(message)
        if message['message_type'] == "group" and post_type == "message":
            await self.__group_message_dispose(message)

    async def __private_message_dispose(self, message):
        re_obj, ma_obj = PluginMatching.find_matching(message['raw_message'], 'private')

        if not ma_obj:
            return

        if plugin := PluginManager.get_plugin_by_name(ma_obj.plugin_name):

            # 传递参数
            self.plugin_parameter["message_info"] = message
            self.plugin_parameter["re_obj"] = re_obj
            self.plugin_parameter["ma_obj"] = ma_obj
            # 执行插件开始方法
            logger.info(f"执行插件：{ma_obj.plugin_name}")
            return await plugin.start(self.plugin_parameter)
        return

    async def __group_message_dispose(self, message):

        re_obj, ma_obj = PluginMatching.find_matching(message['raw_message'], 'group')

        if not ma_obj:
            return

        if plugin := PluginManager.get_plugin_by_name(ma_obj.plugin_name):

            # 传递参数
            self.plugin_parameter["message_info"] = message
            self.plugin_parameter["re_obj"] = re_obj
            self.plugin_parameter["ma_obj"] = ma_obj
            # 执行插件开始方法
            logger.info(f"执行插件：{ma_obj.plugin_name}")
            return await plugin.start(self.plugin_parameter)
        return
