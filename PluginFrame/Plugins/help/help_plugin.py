from aiocqhttp import MessageSegment
from PluginFrame.Plugins import BaseComponentPlugin
from PluginFrame.plugin_constant import code_qq, get_manager_qq, plugin_constant
from PluginFrame.plugins_conf import registration_directive
from utils.text_to_img import to_image
from utils.html_to_image import html_to_png


@registration_directive(matching=r'#菜单(.*)', message_types=("private", "group"))
class MenuPlugin(BaseComponentPlugin):
    __name__ = 'MenuPlugin'
    plu_name = '帮助插件'
    desc = "功能菜单"
    docs = "#菜单"
    permissions = ("all",)

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        # 获取机器人对象
        bot = message_parameter.get("bot")
        re_obj = message_parameter.get("re_obj")
        text = re_obj.group(1)

        if text in plugin_constant.plugins.keys():
            info = f'# {text}插件菜单：\n'
            menu_info = '### 普通用户权限功能菜单如下：\n'
            code_menu_info = '\n### 开发者权限菜单如下：\n'
            manager_menu_info = '\n### 管理员权限菜单如下：\n'
            plugin_desc_name = plugin_constant.plugins.get(text)
            for key, value in plugin_desc_name.items():
                plugin_info = plugin_constant.plugin_desc.get(key)
                if not plugin_info.get('docs'):
                    continue

                if event.message_type in plugin_info.get('message_types'):
                    permissions = plugin_info.get('permissions')
                    if not permissions or 'all' in permissions:
                        menu_info += f"- {key} -- {plugin_info.get('docs')}\n- - -\n"
                        continue
                    if "admin" in permissions:
                        if event.user_id in get_manager_qq():
                            manager_menu_info += f"- {key} -- {plugin_info.get('docs')}\n- - -\n"
                            continue
                    if 'code' in permissions:
                        if event.user_id == code_qq:
                            code_menu_info += f"- {key} -- {plugin_info.get('docs')}\n- - -\n"
                        continue
                    if event.user_id in permissions:
                        menu_info += f"- {key} -- {plugin_info.get('docs')}\n- - -\n"
                        continue
            image_info = await to_image(
                info+menu_info+manager_menu_info+code_menu_info,
                qr_code="https://file.52xiaobei.cn/bFxrC3Wet70up4PB4sFV1FCXHCsud4JA/logo.png"
            )
            resp = MessageSegment.image(f"base64://{image_info}")
            await bot.send(event, resp)


@registration_directive(matching=r'#插件列表', message_types=("private", "group"))
class ListPlugin(BaseComponentPlugin):
    __name__ = 'ListPlugin'
    plu_name = '帮助插件'
    desc = "插件列表"
    docs = "#插件列表"
    permissions = ("all",)

    async def start(self, message_parameter):
        event = message_parameter.get("event")
        # 获取机器人对象
        bot = message_parameter.get("bot")
        image_base64 = html_to_png("help", plugin_constant.plugins)
        resp = MessageSegment.image(f"base64://{image_base64}")
        await bot.send(event, resp)
