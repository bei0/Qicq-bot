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
    api_root: Optional[str] = None
    manager_qq: int


class MessageConfig(BaseModel):
    text_to_image: bool


class ApiConfig(BaseModel):
    key: str
    proxy: str


class GPT3Params(BaseModel):
    temperature: float = 1
    max_tokens: int = 3000
    top_p: float = 1
    presence_penalty: float = 1.0
    frequency_penalty: float = -1.0


class ChatGptConfig(BaseModel):
    Api: Optional[List[ApiConfig]]


class BaaiConfig(BaseModel):
    apiKey: str


class PrConfig(ProjectConfig):
    server: Optional[ServerConfig] = None
    chatGpt: Optional[ChatGptConfig] = None
    gpt_params: Optional[GPT3Params] = None
    message: Optional[MessageConfig] = None
    baai: Optional[BaaiConfig] = None

    @staticmethod
    def config_load():
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        if not os.path.exists(config_path):
            raise FileNotFoundError(f'config.yaml not found in {os.path.dirname(__file__)}')
        with open(config_path, 'r', encoding='utf-8') as f:
            y = yaml.full_load(f)
        Config.server = ServerConfig(**y['server'])
        Config.message = MessageConfig(**y['message'])
        Config.baai = BaaiConfig(**y['baai'])
        # Config.gpt_params = GPT3Params(**y['gpt_params'])

        api_list = []
        for api in y.get('chatGpt', []):
            api_list.append(ApiConfig(**api['Api']))
        Config.chatGpt = ChatGptConfig(Api=api_list)


Config = PrConfig()
