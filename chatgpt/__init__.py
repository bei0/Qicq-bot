import itertools
from typing import Generator
import openai
import requests
from typing import List, Dict
from loguru import logger
from config import Config
from tinydb import TinyDB, Query
import hashlib


class BotManager:
    """Bot lifecycle manager."""
    cache_db = TinyDB('data/login_caches.json')
    bots: Dict[str, List] = {
        "openai-api": [],
    }
    roundrobin: Dict[str, itertools.cycle] = {}

    def __init__(self):
        self.login()

    def login(self):
        self.login_openai()
        count = sum(len(v) for v in self.bots.values())
        if count < 1:
            logger.error("没有登录成功的账号，程序无法启动！")
            exit(-2)
        else:
            # 输出登录状况
            for k, v in self.bots.items():
                logger.info(f"AI 类型：{k} - 可用账号： {len(v)} 个")

    def login_openai(self):
        counter = 0
        for i, account in enumerate(Config.chatGpt.Api):
            logger.info("正在登录第 {i} 个 OpenAI 账号", i=i + 1)
            try:
                bot = self.__login_openai_apikey(account)
                self.bots["openai-api"].append(bot)
            except Exception as e:
                logger.error(e)
                logger.error("登录失败，跳过此账号。")
                continue
            counter += 1
        logger.success(f"成功登录 {counter} 个 OpenAI 账号")

    def __save_login_cache(self, account, cache: dict):
        """保存登录缓存"""
        account_sha = hashlib.sha256(account.json().encode('utf8')).hexdigest()
        q = Query()
        self.cache_db.upsert({'account': account_sha, 'cache': cache}, q.account == account_sha)

    def __load_login_cache(self, account):
        """读取登录缓存"""
        account_sha = hashlib.sha256(account.json().encode('utf8')).hexdigest()
        q = Query()
        cache = self.cache_db.get(q.account == account_sha)
        return cache['cache'] if cache is not None else dict()

    def __login_openai_apikey(self, account):
        logger.info("尝试使用 api_key 登录中...")
        logger.info("当前检查的 API Key 为：" + account.key[:8] + "*********" + account.key[-4:])

        return account

    def pick(self, type: str):
        if not type in self.roundrobin:
            self.roundrobin[type] = itertools.cycle(self.bots[type])
        if len(self.bots[type]) == 0:
            raise ValueError(type)
        return next(self.roundrobin[type])


class BotAdapter:
    """定义所有 Chatbot 的通用接口"""
    preset_name: str = "default"

    def get_queue_info(self): ...
    """获取内部队列"""

    def __init__(self, session_id: str = "unknown"): ...

    async def ask(self, msg: str) -> Generator[str, None, None]: ...
    """向 AI 发送消息"""

    async def rollback(self): ...
    """回滚对话"""

    async def on_reset(self): ...
    """当会话被重置时，此函数被调用"""

    async def preset_ask(self, role: str, text: str): ...
    """以预设方式进行提问"""
