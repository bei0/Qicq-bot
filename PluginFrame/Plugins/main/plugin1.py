from PluginFrame.PluginManager import ModelMenuObj


class Plugin(ModelMenuObj):
    __name__ = 'Plugin'

    def __init__(self):
        pass

    # 实现接入点的接口
    def start(self):
        print(Plugin.all_plugins)
        print(ModelMenuObj.get_plugin_by_name("plugin1.Plugin"))
        print("I am plugin1 , I am a menu!")