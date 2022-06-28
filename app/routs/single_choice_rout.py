from fastapi import APIRouter, Depends
from typing import List

from app.services.single_choice_service import SingleChoiceService 
from app.schemas.states_schemas import SingleChoice, SingleChoiceCreate, SingleChoiceUpdate
from app.services.token_service import verify_token

single_choice_router = APIRouter(prefix="/state/single_choice", tags=["Single Choice State"])

@single_choice_router.post("/create", response_model = SingleChoice)
async def single_choice_create(new_state:SingleChoiceCreate, current_user = Depends(verify_token)):
        return await SingleChoiceService.create(state_model=new_state, user=current_user)

@single_choice_router.get("/all/{chat_id}", response_model = List[SingleChoice])
async def single_choice_get_all(chat_id:int, current_user = Depends(verify_token)):
        return await SingleChoiceService.get_all(chat_id=chat_id, user=current_user)

@single_choice_router.get("/{id}", response_model = SingleChoice)
async def single_choice_get_by_id(id:int, current_user = Depends(verify_token)):
        return await SingleChoiceService.get_by_id(state_id=id)

@single_choice_router.post("/update/{id}")
async def single_choice_update(id:int, update_data:SingleChoiceUpdate, current_user = Depends(verify_token)):
        return await SingleChoiceService.update(state_id=id, update_data=update_data)

@single_choice_router.delete("/delete/{id}")
async def single_choice_delete(id:int, current_user = Depends(verify_token)):
        return await SingleChoiceService.delete(state_id = id)
