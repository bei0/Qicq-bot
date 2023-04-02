import os
from typing import Optional, List
import yaml
from pydantic import BaseModel, validator


class ProjectConfig(BaseModel):
    name: str = 'QicqBot'
    version: str = '0.0.1'
    BasePath: str = os.path.dirname((os.path.abspath(__file__)))


class ServerConfig(BaseModel):
    port: int
    host: str


class CqhttpHttpConfig(BaseModel):
    host: str
    port: int


class CqhttpConfig(BaseModel):
    cqType: str
    http: Optional[CqhttpHttpConfig] = None

    @validator('cqType')
    def verify_cqType(cls, value):
        if value not in ['http', 'ws']:
            raise ValueError('cqType must be http or ws')
        return value


class ApiConfig(BaseModel):
    key: str
    proxy: str


class ChatGptConfig(BaseModel):
    Api: Optional[List[ApiConfig]]


class PrConfig(ProjectConfig):
    server: Optional[ServerConfig] = None
    cqhttp: Optional[CqhttpConfig] = None
    chatGpt: Optional[ChatGptConfig] = None

    @staticmethod
    def config_load():
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        if not os.path.exists(config_path):
            raise FileNotFoundError(f'config.yaml not found in {os.path.dirname(__file__)}')
        with open(config_path, 'r', encoding='utf-8') as f:
            y = yaml.full_load(f)
        Config.server = ServerConfig(**y['server'])

        api_list = []
        for api in y.get('chatGpt', []):
            api_list.append(ApiConfig(**api['Api']))
        Config.chatGpt = ChatGptConfig(Api=api_list)

        Config.cqhttp = CqhttpConfig(**y['cqhttp'])


Config = PrConfig()
