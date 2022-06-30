import socket
import sys

from fastapi import FastAPI
import app.routs as routs 
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

app.include_router(routs.login_router)
app.include_router(routs.creator_user_router)
app.include_router(routs.chatbot_router)
app.include_router(routs.base_state_router)
app.include_router(routs.single_choice_router)
app.include_router(routs.multiple_choice_router)
