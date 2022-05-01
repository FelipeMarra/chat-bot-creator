import socket
import sys

from fastapi import FastAPI
from app.views.user_view import user_router

#start app
app = FastAPI()

hostname = socket.gethostname()

version = f"{sys.version_info.major}.{sys.version_info.minor}"


#add routs
@app.get("/")
async def read_root():
    return {
        "name": "chat-bot-creator-back",
        "host": hostname,
        "version": f"Hello world! From FastAPI running on Uvicorn. Using Python {version}"
    }

app.include_router(user_router)

