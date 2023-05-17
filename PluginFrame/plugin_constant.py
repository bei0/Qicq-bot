# 命令关联的插件
import json
import os
import pickle
from config import Config
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PluginConstant:
    __directives = {}
    # 命令插件索引
    __directives_keys = {
        "private": [],
        "group": []
    }
    # 插件集合
    __plugins = {}
    # 插件描述
    __plugin_desc = {}
    # 插件描述索引
    __plugin_desc_key = {}

    @property
    def directives(self):
        return self.__directives

    @property
    def directives_keys(self):
        return self.__directives_keys

    @property
    def plugins(self):
        return self.__plugins

    @property
    def plugin_desc(self):
        return self.__plugin_desc

    @property
    def plugin_desc_key(self):
        return self.__plugin_desc_key

    def add_directives(self, key, value):
        self.__directives[key] = value

    def add_directives_keys(self, key, value):
        if key not in ("private", "group"):
            raise ValueError("Key 未找到")
        self.__directives_keys[key].append(value)

    def add_plugins(self, key, value):
        self.__plugins[key] = value

    def add_plugin_desc(self, key, value):
        self.__plugin_desc[key] = value

    def add_plugin_desc_key(self, key, value):
        self.__plugin_desc_key[key] = value

    def del_directives(self):
        self.__directives = {}

    def del_directives_keys(self):
        self.__directives_keys = {"private": [], "group": []}

    def del_plugins(self):
        self.__plugins = {}

    def del_plugin_desc(self):
        self.__plugin_desc = {}

    def del_plugin_desc_key(self):
        self.__plugin_desc_key = {}


plugin_constant = PluginConstant()

manager_qq = [Config.server.manager_qq, ]

code_qq = Config.server.manager_qq

black_list = {
    "private": [],
    "group": []
}

choose_data = {}


def init_manager_qq():
    if not os.path.isfile(os.path.join(path, "data/manager_qq.json")):
        with open(os.path.join(path, "data/manager_qq.json"), 'wb') as f:
            pickle.dump(manager_qq, f)
    return True


def add_manager_qq(qq):
    manager_qq.append(qq)

    with open(os.path.join(path, "data/manager_qq.json"), 'wb') as f:
        pickle.dump(manager_qq, f)

    return True


def get_manager_qq():
    global manager_qq
    if os.path.isfile(os.path.join(path, "data/manager_qq.json")):
        with open(os.path.join(path, "data/manager_qq.json"), 'rb') as f:
            manager_qq = pickle.load(f)
    return manager_qq


def set_choose_data(user_id, message_type, key, value):
    del_choose_data(user_id)

    choose_data[f"{user_id}"] = {
        f"{message_type}": {
            key: value
        }
    }
    with open(os.path.join(path, "data/choose_data.json"), 'w') as f:
        json.dump(choose_data, f)
    return True


def get_choose_data(user_id, message_type):
    global choose_data

    if os.path.isfile(os.path.join(path, "data/choose_data.json")):
        with open(os.path.join(path, "data/choose_data.json"), 'r') as f:
            choose_data = json.load(f)

    if str(user_id) in choose_data:
        if message_type in choose_data[str(user_id)]:
            return choose_data[str(user_id)][message_type]
    return {}


def del_choose_data(user_id, ):
    if str(user_id) in choose_data:
        choose_data.pop(str(user_id))

    with open(os.path.join(path, "data/choose_data.json"), 'w') as f:
        json.dump(choose_data, f)

    return True


def set_black_list(black_type, black):
    black_list[black_type].append(black)

    with open(os.path.join(path, "data/black_list.json"), 'w') as f:
        json.dump(black_list, f)
    return True


def get_black_list(black_type):
    global black_list

    if os.path.isfile(os.path.join(path, "data/black_list.json")):
        with open(os.path.join(path, "data/black_list.json"), 'r') as f:
            black_list = json.load(f)
    return black_list[black_type]


def del_black_list(black_type, black):
    global black_list
    black_list_new = get_black_list(black_type)
    if black in black_list_new:
        black_list_new.pop(black_list_new.index(black))

    black_list[black_type] = black_list_new

    with open(os.path.join(path, "data/black_list.json"), 'w') as f:
        json.dump(black_list, f)

    return True


def reset_plugins():
    plugin_constant.del_plugins()
    plugin_constant.del_plugin_desc()
    plugin_constant.del_plugin_desc_key()
    plugin_constant.del_directives()
    plugin_constant.del_directives_keys()