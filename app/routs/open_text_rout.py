from fastapi import APIRouter, Depends
from typing import List

from app.services.open_text_service import OpenTextService 
from app.schemas.states_schemas import OpenText, OpenTextCreate, OpenTextUpdate
from app.services.token_service import verify_token

open_text_router = APIRouter(prefix="/state/open_text", tags=["Open Text  State"])

@open_text_router.post("/create", response_model = OpenText)
async def multiple_choice_create(new_state:OpenTextCreate, current_user = Depends(verify_token)):
        return await OpenTextService.create(state_model=new_state, user=current_user)

@open_text_router.get("/all/{chat_id}", response_model = List[OpenText])
async def multiple_choice_get_all(chat_id:int, current_user = Depends(verify_token)):
        return await OpenTextService.get_all(chat_id=chat_id, user=current_user)

@open_text_router.get("/{id}", response_model = OpenText)
async def multiple_choice_get_by_id(id:int, current_user = Depends(verify_token)):
        return await OpenTextService.get_by_id(state_id=id)

@open_text_router.post("/update/{id}")
async def multiple_choice_update(id:int, update_data:OpenTextUpdate, current_user = Depends(verify_token)):
        return await OpenTextService.update(state_id=id, update_data=update_data)

@open_text_router.delete("/delete/{id}")
async def multiple_choice_delete(id:int, current_user = Depends(verify_token)):
        return await OpenTextService.delete(state_id = id)
