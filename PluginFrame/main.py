

if __name__ == '__main__':
    from PluginFrame.PluginManager import PluginManager
    from PluginFrame.PluginManager import __ALLMODEL__
    # 加载所有插件
    PluginManager.load_all_plugin()

    # 遍历所有接入点下的所有插件
    for SingleModel in __ALLMODEL__:
        plugins = SingleModel.get_plugin_object()
        for item in plugins:

            # 调用接入点的公共接口
            item.start()
