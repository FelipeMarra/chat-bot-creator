from fastapi import APIRouter, Depends
from typing import List

from app.services.chat_bot_service import ChatBotService 
from app.schemas.chats_schemas import ChatBotCreate, ChatBot, ChatBotUpdate
from app.services.token_service import verify_token

chatbot_router = APIRouter(prefix="/chatbot", tags=["Chat Bots"])

@chatbot_router.post("/create", response_model = ChatBot)
async def chatbot_create(chat_bot:ChatBotCreate, current_user = Depends(verify_token)):
        return await ChatBotService.create(name=chat_bot.name, user=current_user)

@chatbot_router.get("/all", response_model = List[ChatBot])
async def chatbot_get_all(current_user = Depends(verify_token)):
        return await ChatBotService.get_all(user=current_user)

@chatbot_router.get("/{id}", response_model = ChatBot)
async def chatbot_get_by_id(id:int, current_user = Depends(verify_token)):
        return await ChatBotService.get_by_id(chatbot_id=id)

@chatbot_router.post("/update/{id}")
async def chatbot_update(id:int, update_data:ChatBotUpdate, current_user = Depends(verify_token)):
        return await ChatBotService.update(id, update_data)

@chatbot_router.delete("/delete/{id}")
async def user_create(id:int, current_user = Depends(verify_token)):
        return ChatBotService.delete(chatbot_id = id)
