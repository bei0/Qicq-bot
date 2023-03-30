import os
from typing import Optional, List
from loguru import logger
import yaml
from pydantic import BaseModel


class ProjectConfig(BaseModel):
    name: str = 'QicqBot'
    version: str = '0.0.1'
    BasePath: str = os.path.dirname((os.path.abspath(__file__)))


class ServerConfig(BaseModel):
    port: int
    host: str


class ApiConfig(BaseModel):
    key: str


class ChatGptConfig(BaseModel):
    Api: Optional[List[ApiConfig]]


class PrConfig(ProjectConfig):
    server: Optional[ServerConfig] = None
    chatGpt: Optional[ChatGptConfig] = None

    @staticmethod
    def config_load():
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        if not os.path.exists(config_path):
            raise FileNotFoundError(f'config.yaml not found in {os.path.dirname(__file__)}')
        with open(config_path, 'r') as f:
            y = yaml.full_load(f)
        Config.server = ServerConfig(**y['server'])

        api_list = []
        for api in y.get('chatGpt', []):
            api_list.append(ApiConfig(**api['Api']))
        Config.chatGpt = ChatGptConfig(Api=api_list)


Config = PrConfig()
