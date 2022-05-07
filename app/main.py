import socket
import sys

from fastapi import FastAPI
from app.routs.login_rout import login_router
from app.routs.user_rout import user_router
from fastapi.middleware.cors import CORSMiddleware

#start app
app = FastAPI()

hostname = socket.gethostname()

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#add routs
@app.get("/")
async def read_root():
    return {
        "name": "chat-bot-creator-back",
        "host": hostname,
        "version": f"Chat Bot Creator From FastAPI running on Uvicorn. Using Python {version}"
    }

app.include_router(login_router)
app.include_router(user_router)

