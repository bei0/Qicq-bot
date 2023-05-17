import asyncio
from config import Config


async def start_task():
    """|coro|
    以异步方式启动
    """
    from PluginFrame.PluginManager import PluginManager
    PluginManager.load_all_plugin()

    from PluginFrame.plugin_constant import init_manager_qq
    init_manager_qq()

    from PluginFrame.chace_data import init_cache
    init_cache()

    from cqhttp import bot
    from message.message_dispose import MessageDispose
    from message.notice_dispose import NoticeDispose
    bot.on_message()(MessageDispose().dispose)
    bot.on_notice()(NoticeDispose().dispose)
    return await bot.run_task(host=Config.server.host, port=Config.server.port, use_reloader=True)


Config.config_load()
loop = asyncio.get_event_loop()
loop.run_until_complete(start_task())
