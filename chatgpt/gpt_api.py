from revChatGPT.V3 import Chatbot
from config import Config

chatbot = Chatbot(api_key=Config.chatGpt.Api[0].key, proxy=Config.chatGpt.Api[0].proxy or None)

