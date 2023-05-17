from PluginFrame.Plugins import BaseComponentPlugin
from PluginFrame.plugin_constant import code_qq, get_manager_qq, add_manager_qq,\
    get_black_list, set_black_list, del_black_list
from PluginFrame.plugins_conf import registration_directive


@registration_directive(matching=r'#禁用此群', message_types=("group",))
class AddGroupBlacklistPlugin(BaseComponentPlugin):
    __name__ = 'AddGroupBlacklistPlugin'
    plu_name = 'BOT管理插件'
    desc = "将某群加入黑名单"
    docs = "#禁用此群"
    permissions = ("code",)

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        # 获取机器人对象
        bot = message_parameter.get("bot")

        if event.group_id in get_black_list("group"):
            return

        set_black_list("group", event.group_id)

        await bot.send(event, "添加成功！")
        return True


@registration_directive(matching=r'#解禁此群', message_types=("group",))
class DelGroupBlacklistPlugin(BaseComponentPlugin):
    __name__ = 'DelGroupBlacklistPlugin'
    plu_name = 'BOT管理插件'
    desc = "将某群移除黑名单"
    docs = "#解禁此群"
    permissions = ("code",)

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        # 获取机器人对象
        bot = message_parameter.get("bot")

        if event.group_id in get_black_list("group"):
            del_black_list("group", event.group_id)
            await bot.send(event, "解禁成功！")
        else:
            return


@registration_directive(matching=r'#添加管理员(\d+|\[CQ:at,qq=(\d+)\])', message_types=("private", "group"))
class AddManagerPlugin(BaseComponentPlugin):
    __name__ = 'AddManagerPlugin'
    plu_name = 'BOT管理插件'
    desc = "添加机器人管理员"
    docs = "#添加管理员[@群员 | QQ号]"
    permissions = ("code",)

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        # 获取正则对象
        re_obj = message_parameter.get("re_obj")
        # 获取机器人对象
        bot = message_parameter.get("bot")
        friends_qq, at_qq = re_obj.groups()

        if at_qq:
            if int(at_qq) not in get_manager_qq():
                add_manager_qq(int(at_qq))
            else:
                await bot.send(event, "已经是管理员！")
                return
        else:
            if int(friends_qq) not in get_manager_qq():
                add_manager_qq(int(friends_qq))
            else:
                await bot.send(event, "已经是管理员！")
                return

        await bot.send(event, "添加成功！")
        return True


@registration_directive(matching=r'#禁用(\d+|\[CQ:at,qq=(\d+)\])', message_types=("private", "group"))
class AddFriendBlacklistPlugin(BaseComponentPlugin):
    __name__ = 'AddFriendBlacklistPlugin'
    plu_name = 'BOT管理插件'
    desc = "禁用某QQ使用机器人"
    docs = "#禁用[@群员 | QQ号]"
    permissions = ("admin", )

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        # 获取正则对象
        re_obj = message_parameter.get("re_obj")
        # 获取机器人对象
        bot = message_parameter.get("bot")
        friends_qq, at_qq = re_obj.groups()

        if at_qq:
            if int(at_qq) == code_qq:
                await bot.send(event, "禁止将开发者添加黑名单！")
                return
            if int(at_qq) in get_manager_qq():
                if event.user_id == code_qq:
                    set_black_list("private", int(at_qq))
                    return
                else:
                    await bot.send(event, "无权限将管理员加入黑名单！")
                    return
            set_black_list("private", int(at_qq))
        else:
            if int(friends_qq) == code_qq:
                await bot.send(event, "禁止将开发者添加黑名单！")
                return
            if int(friends_qq) in get_manager_qq():
                if event.user_id == code_qq:
                    set_black_list("private", int(friends_qq))
                    return
                else:
                    await bot.send(event, "无权限将管理员加入黑名单！")
                    return
            set_black_list("private", int(friends_qq))

        await bot.send(event, "添加成功！")
        return True


@registration_directive(matching=r'#解禁(\d+|\[CQ:at,qq=(\d+)\])', message_types=("private", "group"))
class DelFriendBlacklistPlugin(BaseComponentPlugin):
    __name__ = 'DelFriendBlacklistPlugin'
    plu_name = 'BOT管理插件'
    desc = "移除禁用某QQ使用机器人"
    docs = "#解禁[@群员 | QQ号]"
    permissions = ("admin", )

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        # 获取正则对象
        re_obj = message_parameter.get("re_obj")
        # 获取机器人对象
        bot = message_parameter.get("bot")
        friends_qq, at_qq = re_obj.groups()

        if at_qq:
            if int(at_qq) in get_manager_qq():
                if event.user_id == code_qq:
                    del_black_list("private", int(at_qq))
                else:
                    await bot.send(event, "无权限将管理员移除黑名单！")
                    return
            del_black_list("private", int(at_qq))
        else:
            if int(friends_qq) in get_manager_qq():
                if event.user_id == code_qq:
                    del_black_list("private", int(friends_qq))
                else:
                    await bot.send(event, "无权限将管理员移除黑名单！")
                    return
            del_black_list("private", int(friends_qq))

        await bot.send(event, "移除成功！")
        return True