import re
import dataclasses
from loguru import logger


class DirectivesPluginMeta(type):
    _directives = {}
    _directives_keys = {
        "private": [],
        "group": []
    }

    def __init__(cls, _class_name, _base, _class_obj, **kwargs):
        for key, value in _class_obj.items():
            if isinstance(value, DirectivesField):
                if value.matching in cls._directives_keys:
                    raise ValueError(f"指令 {value.matching} 已存在")
                cls._directives[key] = value
                for message_type in value.message_types:
                    cls._directives_keys[message_type].append(value.matching)
        super(DirectivesPluginMeta, cls).__init__(_class_name, _base, _class_obj, **kwargs)

    @property
    def directives(self):
        return self._directives

    def find_matching(self, matching, message_type):
        directive, match_obj = None, None
        for key, value in self._directives.items():
            if re.fullmatch(value.matching, matching) and message_type in value.message_types:
                match_obj = re.fullmatch(value.matching, matching)
                directive = value
        return match_obj, directive

    def __setattr__(cls, key, value):
        for message_type in value.message_types:
            if value.matching in cls._directives_keys[message_type]:
                raise ValueError(f"指令 {value.matching} 已存在 {message_type}")
        cls._directives[key] = value
        for message_type in value.message_types:
            cls._directives_keys[message_type].append(value.matching)
        return True


@dataclasses.dataclass
class DirectivesField:
    matching: str = '.*'
    plugin_name: str = None
    message_types: tuple = ("private", "group")


class PluginMatching(metaclass=DirectivesPluginMeta):
    ...


# class MessageMatching(PluginMatching):
#     # 通用聊天匹配（没有匹配其他指令就会走这个）
#     private_message = DirectivesField(matching=r'^(?![-.])(.*)', plugin_name="privateMessage", message_types=("private",))
#     group_message = DirectivesField(
#         matching=r'\[CQ:(\w+),qq=(\w+)] (.*)', plugin_name="groupMessage", message_types=("group",)
#     )
#     findApiLines = DirectivesField(matching=r'\.查询API额度', plugin_name="findApiLines", message_types=("private", ))


def registration_directive(matching: str, message_types: tuple):
    def wrapper(cls):
        plugin_name = cls.__name__
        setattr(
            PluginMatching,
            plugin_name,
            DirectivesField(matching=matching, plugin_name=plugin_name, message_types=message_types)
        )
        logger.info(f"注册{','.join(message_types)}指令：{plugin_name} - {matching}")
    return wrapper





