from fastapi import FastAPI

from api.v1.cqhttp_socket import cqhttp

app = FastAPI()

app.include_router(cqhttp)

if __name__ == "__main__":
    import uvicorn
    # 官方推荐是用命令后启动 uvicorn main:app --host=127.0.0.1 --port=8010 --reload
    uvicorn.run(app='main:app', host="0.0.0.0", port=6555, reload=True)
