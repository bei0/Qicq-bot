from fastapi import FastAPI
from loguru import logger

from PluginFrame.PluginManager import PluginManager, __ALLMODEL__
from api.v1.cqhttp_socket import cqhttp
from config import Config

# 加载配置文件
Config.config_load()
# 创建fastapi实例
app = FastAPI()
# 加载所有插件
app.add_event_handler("startup", PluginManager.load_all_plugin)

# 路由
app.include_router(cqhttp)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app', host=Config.server.host, port=Config.server.port, reload=True, workers=10)
