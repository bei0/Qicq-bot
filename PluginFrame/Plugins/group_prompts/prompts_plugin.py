from PluginFrame.Plugins import BaseComponentPlugin
from PluginFrame.chace_data import set_cache, get_cache, del_cache
from PluginFrame.plugins_conf import registration_directive


@registration_directive(matching=r'#设置入群提示语 (.*)', message_types=("group", ))
class GroupPromptPlugin(BaseComponentPlugin):
    __name__ = 'GroupPromptPlugin'
    plu_name = 'QQ群提示插件'
    desc = "设置入群提示语 【提示语文本】"
    docs = '#设置入群提示语 [提示文本(支持CQ转义)]'
    permissions = ("admin",)

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        re_obj = message_parameter.get("re_obj")
        text = re_obj.group(1)

        set_cache(str(event.group_id), text)

        await bot.send(event, "添加成功")


@registration_directive(matching=r'#删除入群提示语', message_types=("group", ))
class DelGroupPromptPlugin(BaseComponentPlugin):
    __name__ = 'DelGroupPromptPlugin'
    plu_name = 'QQ群提示插件'
    desc = "删除入群提示语"
    docs = '#删除入群提示语'
    permissions = ("admin",)

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        if get_cache(str(event.group_id)):
            del_cache(str(event.group_id))

        await bot.send(event, "删除成功")


@registration_directive(matching=r'#开启退群提醒', message_types=("group", ))
class GroupExitPlugin(BaseComponentPlugin):
    __name__ = 'GroupExitPlugin'
    plu_name = 'QQ群提示插件'
    desc = "开启退群提醒"
    docs = '#开启退群提醒'
    permissions = ("admin",)

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        bot = message_parameter.get("bot")

        infos = get_cache("group_exit") or []
        if event.group_id not in infos:
            infos.append(event.group_id)
            set_cache("group_exit", infos)
        await bot.send(event, "添加成功")


@registration_directive(matching=r'#关闭退群提醒', message_types=("group", ))
class DelGroupExitPlugin(BaseComponentPlugin):
    __name__ = 'DelGroupExitPlugin'
    plu_name = 'QQ群提示插件'
    desc = "关闭退群提醒"
    docs = '#关闭退群提醒'
    permissions = ("admin",)

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        bot = message_parameter.get("bot")
        infos = get_cache("group_exit") or []
        if event.group_id in infos:
            infos.pop(infos.index(event.group_id))
            set_cache("group_exit", infos)

        await bot.send(event, "删除成功")
