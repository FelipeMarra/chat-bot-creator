from fastapi import APIRouter, Depends
from typing import List

from app.services.base_state_service import StateBaseService 
from app.schemas.states_schemas import StateBase, StateBaseCreate, StateBaseUpdate
from app.services.token_service import verify_token

base_state_router = APIRouter(prefix="/state/base", tags=["Chat Base State"])

@base_state_router.post("/create", response_model = StateBase)
async def state_create(new_state:StateBaseCreate, current_user = Depends(verify_token)):
        return await StateBaseService.create(state_model=new_state, user=current_user)

@base_state_router.get("/all/{chat_id}", response_model = List[StateBase])
async def state_get_all(chat_id:int, current_user = Depends(verify_token)):
        return await StateBaseService.get_all(chat_id=chat_id, user=current_user)

@base_state_router.get("/{id}", response_model = StateBase)
async def state_get_by_id(id:int, current_user = Depends(verify_token)):
        return await StateBaseService.get_by_id(state_id=id)

@base_state_router.post("/update/{id}", response_model = StateBase)
async def state_update(id:int, update_data:StateBaseUpdate, current_user = Depends(verify_token)):
        return await StateBaseService.update(state_id=id, update_data=update_data)

@base_state_router.delete("/delete/{id}")
async def state_delete(id:int, current_user = Depends(verify_token)):
        return await StateBaseService.delete(state_id = id)
