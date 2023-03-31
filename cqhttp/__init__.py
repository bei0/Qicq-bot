from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class ApiField:
    Name: str
    Api: str
    requestBody: BaseModel = None
    RespBody: BaseModel = None

    """
    存储接口信息：https://docs.go-cqhttp.org/api
        Name: 接口名称
        Api: 接口地址
        requestBody: 请求体
        RespBody: 响应体
    """

    def __repr__(self):
        return f"{self.Name}({self.Api})"

    def __str__(self):
        return f"{self.Name}({self.Api})"


class SendMsgModel(BaseModel):
    action: str
    params: dict
    echo: str


class SendHttpMsgModel(BaseModel):
    ...
