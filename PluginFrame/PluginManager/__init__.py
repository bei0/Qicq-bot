import abc
import os
import sys
from imp import find_module
from imp import load_module
from loguru import logger

bash_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PluginManager(type):
    # 静态变量配置插件路径
    __PluginPath = 'Plugins'
    __name__ = 'Plugins'

    # 调用时将插件注册
    def __init__(self, _name, _bases, _dict):
        if not hasattr(self, '_AllPlugins'):
            self._AllPlugins = {}
        else:
            self.register_all_plugin(self)
        super(PluginManager, self).__init__(_name, _bases, _dict)

    # 设置插件路径
    @staticmethod
    def set_plugin_path(path):
        if os.path.isdir(path):
            PluginManager.__PluginPath = path
        else:
            print('%s is not a valid path' % path)

    # 递归检测插件路径下的所有插件，并将它们存到内存中
    @staticmethod
    def load_all_plugin():
        plugin_path = os.path.join(bash_path, PluginManager.__PluginPath)
        if not os.path.isdir(plugin_path):
            raise EnvironmentError('%s is not a directory' % plugin_path)
        items = os.listdir(plugin_path)
        for item in items:

            if os.path.isdir(os.path.join(plugin_path, item)):
                PluginManager.__PluginPath = os.path.join(plugin_path, item)
                PluginManager.load_all_plugin()
            else:
                if item.endswith('.py') and item != '__init__.py':
                    module_name = item[:-3]
                    if module_name not in sys.modules:
                        file_handle, file_path, dect = find_module(module_name, [plugin_path])
                    try:
                        load_module(module_name, file_handle, file_path, dect)
                    finally:
                        if file_handle: file_handle.close()

    # 返回所有的插件
    @property
    def all_plugins(self):
        return self._AllPlugins

    # 注册插件
    def register_all_plugin(self, a_plugin):
        assert not a_plugin.__name__ in self._AllPlugins, "Plugin %s already registered" % a_plugin.__name__
        plugin_obj = a_plugin()
        logger.info(f"加载插件：{a_plugin.__name__}")
        self._AllPlugins[a_plugin.__name__] = plugin_obj

    # 注销插件
    def unregister_plugin(self, plugin_name):
        if plugin_name in self._AllPlugins:
            plugin_obj = self._AllPlugins[plugin_name]
            del plugin_obj

    # 获取插件对象。
    def get_plugin_object(self, plugin_name=None):
        if plugin_name is None:
            return self._AllPlugins.values()
        else:
            result = self._AllPlugins[plugin_name] if plugin_name in self._AllPlugins else None
            return result

    # 根据插件名字，获取插件对象。（提供插件之间的通信）
    @staticmethod
    def get_plugin_by_name(plugin_name):
        if plugin_name is None:
            return None
        else:
            for SingleModel in __ALLMODEL__:
                plugin = SingleModel.get_plugin_object(plugin_name)
                if plugin:
                    return plugin


# 插件框架的接入点。便于管理各个插件。各个插件通过继承接入点类，利用Python中metaclass的优势，将插件注册。接入点中定义了各个插件模块必须要实现的接口。
class ModelComponent(metaclass=PluginManager):
    __name__ = 'ModelComponent'

    @abc.abstractmethod
    def start(self, message_parameter):
        print('Please write the Start() function')


class ModelMenuObj(metaclass=PluginManager):
    __name__ = 'ModelMenuObj'

    def start(self, message_parameter):
        print('Please write the Start() function')


class ModelToolBarObj(metaclass=PluginManager):
    __name__ = 'ModelToolBarObj'

    def start(self, message_parameter):
        print('Please write the Start() function')


class ModelParamPanelObj(metaclass=PluginManager):
    __name__ = 'ModelParamPanelObj'

    def start(self, message_parameter):
        print('Please write the Start() function')


__ALLMODEL__ = (ModelParamPanelObj, ModelToolBarObj, ModelMenuObj, ModelComponent)