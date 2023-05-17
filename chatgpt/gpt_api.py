import ctypes
import json

from janus import Queue
from loguru import logger
from revChatGPT.V3 import Chatbot as OpenAIChatbot
from starlette.background import BackgroundTasks

from chatgpt import BotAdapter, BotManager
from config import Config
from cqhttp.api import CQApiConfig
from cqhttp.cq_code import CqReply
from cqhttp.request_model import SendPrivateMsgRequest
from utils.text_to_img import to_image

hashu = lambda word: ctypes.c_uint64(hash(word)).value


class ChatGPTAPIAdapter(BotAdapter):
    api_info: Config.chatGpt.Api = None
    """API Key"""

    bot: OpenAIChatbot = None
    """实例"""

    hashed_user_id: str
    bot_manager = BotManager()

    problem_queue = Queue().sync_q

    def __init__(self, session_id: str = "unknown"):
        self.session_id = session_id
        self.hashed_user_id = "user-" + hashu("session_id").to_bytes(8, "big").hex()
        self.api_info = self.bot_manager.pick('openai-api')
        print(self.api_info)
        self.bot = OpenAIChatbot(
            api_key=self.api_info.key,
            proxy=self.api_info.proxy if self.api_info.proxy else None,
            presence_penalty=Config.gpt_params.presence_penalty,
            frequency_penalty=Config.gpt_params.frequency_penalty,
            top_p=Config.gpt_params.top_p,
            temperature=Config.gpt_params.temperature,
            max_tokens=Config.gpt_params.max_tokens,
        )
        self.conversation_id = None
        self.parent_id = None
        super().__init__()
        self.bot.conversation[self.session_id] = [
            {"role": "system", "content": self.bot.system_prompt}
        ]

    async def on_reset(self):
        self.bot.conversation[self.session_id] = [
            {"role": "system", "content": self.bot.system_prompt}
        ]
        self.api_info = self.bot_manager.pick('openai-api')
        self.bot = OpenAIChatbot(api_key=self.api_info.api_key, proxy=self.api_info.proxy)


chat = ChatGPTAPIAdapter()




