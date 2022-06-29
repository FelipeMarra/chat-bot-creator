from fastapi import APIRouter, Depends
from typing import List

from app.services.multiple_choice_service import MultipleChoiceService 
from app.schemas.states_schemas import MultipleChoice, MultipleChoiceCreate, MultipleChoiceUpdate
from app.services.token_service import verify_token

multiple_choice_router = APIRouter(prefix="/state/single_choice", tags=["Single Choice State"])

@multiple_choice_router.post("/create", response_model = MultipleChoice)
async def multiple_choice_create(new_state:MultipleChoiceCreate, current_user = Depends(verify_token)):
        return await MultipleChoiceService.create(state_model=new_state, user=current_user)

@multiple_choice_router.get("/all/{chat_id}", response_model = List[MultipleChoice])
async def multiple_choice_get_all(chat_id:int, current_user = Depends(verify_token)):
        return await MultipleChoiceService.get_all(chat_id=chat_id, user=current_user)

@multiple_choice_router.get("/{id}", response_model = MultipleChoice)
async def multiple_choice_get_by_id(id:int, current_user = Depends(verify_token)):
        return await MultipleChoiceService.get_by_id(state_id=id)

@multiple_choice_router.post("/update/{id}")
async def multiple_choice_update(id:int, update_data:MultipleChoiceUpdate, current_user = Depends(verify_token)):
        return await MultipleChoiceService.update(state_id=id, update_data=update_data)

@multiple_choice_router.delete("/delete/{id}")
async def multiple_choice_delete(id:int, current_user = Depends(verify_token)):
        return await MultipleChoiceService.delete(state_id = id)
