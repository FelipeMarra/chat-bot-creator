import imp
from fastapi import APIRouter, Depends
from typing import List

from app.services.base_state_service import StateBaseService 
from app.schemas.states_schemas import StateBase, StateBaseCreate
from app.services.token_service import verify_token

base_state_router = APIRouter(prefix="/state/base", tags=["Chat Base State"])

@base_state_router.post("/create", response_model = StateBase)
async def state_create(new_state:StateBaseCreate, current_user = Depends(verify_token)):
        return await StateBaseService.create(state_model=new_state, user=current_user)

# @base_state_router.get("/all", response_model = List[ChatBot])
# async def chatbot_get_all(current_user = Depends(verify_token)):
#         return await ChatBotService.get_all(user=current_user)

# @base_state_router.get("/{id}", response_model = ChatBot)
# async def chatbot_get_by_id(id:int, current_user = Depends(verify_token)):
#         return await ChatBotService.get_by_id(chatbot_id=id)

# @base_state_router.post("/update/{id}", response_model = ChatBot)
# async def chatbot_update(id:int, update_data:ChatBotUpdate, current_user = Depends(verify_token)):
#         return await ChatBotService.update(id, update_data)

# @base_state_router.delete("/delete/{id}")
# async def user_create(id:int, current_user = Depends(verify_token)):
#         await ChatBotService.delete(chatbot_id = id)
#         return "200 OK"