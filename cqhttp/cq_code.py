import dataclasses
from typing import Union, Dict, Optional, Any


class CQCode:

    @classmethod
    def _remove_optional(cls, d: Dict[str, Optional[str]]) -> Dict[str, str]:
        """改变原参数。"""
        for k in tuple(d.keys()):
            if d[k] is None:
                del d[k]
        return d  # type: ignore

    @classmethod
    def _optionally_strfy(cls, x: Optional[Any]) -> Optional[str]:
        if x is not None:
            if isinstance(x, bool):
                x = int(x)  # turn boolean to 0/1
            x = str(x)
        return x

    @classmethod
    def escape(cls, s: str, *, escape_comma: bool = True) -> str:
        """
        对字符串进行 CQ 码转义。

        ``escape_comma`` 参数控制是否转义逗号（``,``）。
        """
        s = s.replace('&', '&amp;') \
            .replace('[', '&#91;') \
            .replace(']', '&#93;')
        if escape_comma:
            s = s.replace(',', '&#44;')
        return s

    @classmethod
    def unescape(cls, s: str) -> str:
        """对字符串进行 CQ 码去转义。"""
        return s.replace('&#44;', ',') \
            .replace('&#91;', '[') \
            .replace('&#93;', ']') \
            .replace('&amp;', '&')

    @classmethod
    def to_cq(cls, type: str, data: Dict[str, Any]) -> str:
        """将消息段转换成字符串格式。"""
        if type == 'text':
            return cls.escape(data.get('text', ''), escape_comma=False)

        params = ','.join(
            ('{}={}'.format(k, cls.escape(str(v))) for k, v in data.items()))
        if params:
            params = ',' + params
        return '[CQ:{type}{params}]'.format(type=type, params=params)


@dataclasses.dataclass
class CqImage(CQCode):
    file: str
    type: str = None
    cache: int = None
    proxy: int = None
    timeout: int = None
    destruct: int = None

    @property
    def cq(self):
        self._remove_optional({
            "file": self.file,
            "type": self._optionally_strfy(self.type),
            "cache": self._optionally_strfy(self.cache),
            "proxy": self._optionally_strfy(self.proxy),
            "timeout": self._optionally_strfy(self.timeout),
            "destruct": self._optionally_strfy(self.destruct),
        })

        cq_text = self.to_cq("image", self._remove_optional({
            "file": self.file,
            "type": self._optionally_strfy(self.type),
            "cache": self._optionally_strfy(self.cache),
            "proxy": self._optionally_strfy(self.proxy),
            "timeout": self._optionally_strfy(self.timeout),
            "destruct": self._optionally_strfy(self.destruct),
        }))

        return cq_text


@dataclasses.dataclass
class CqReply(CQCode):
    id: int = None
    text: str = None
    qq: int = None
    time: int = None
    seq: int = None

    @property
    def cq(self):

        cq_text = self.to_cq("reply", self._remove_optional({
            "id": self.id,
            "text": self._optionally_strfy(self.text),
            "qq": self._optionally_strfy(self.qq),
            "time": self._optionally_strfy(self.time),
            "seq": self._optionally_strfy(self.seq),
        }))

        return cq_text


@dataclasses.dataclass
class CqNode(CQCode):
    id: int = None
    name: str = None
    uin: int = None
    content: str = None

    @property
    def json(self):

        _ = {
            "type": 'node',
            "data": self._remove_optional({
                "id": self.id,
                "name": self._optionally_strfy(self.name),
                "uin": self._optionally_strfy(self.uin),
                "content": self._optionally_strfy(self.content),
                # "seq": self._optionally_strfy(self.content)
            })
        }

        return _


@dataclasses.dataclass
class CqJson(CQCode):
    data: Union[dict, list] = None

    @property
    def cq(self):

        _ = self.to_cq("json", {"data": self.data})

        return _
