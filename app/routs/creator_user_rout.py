from fastapi import APIRouter, Depends

from app.models.users_models import CreatorUser
from app.services.creator_user_service import CreatorUserService 
from app.schemas.users_schemas import CreatorUserCreate, CreatorUser
from app.services.token_service import verify_token

creator_user_router = APIRouter(prefix="/creator_user", tags=["Creator User"])

@creator_user_router.post("/create", response_model = CreatorUser)
async def user_create(user_input:CreatorUserCreate):
        return await CreatorUserService.create(name=user_input.name, email=user_input.email, password=user_input.password)

@creator_user_router.get('/current', response_model = CreatorUser)
async def get_user(current_user = Depends(verify_token)):
        return current_user

@creator_user_router.get('/{id}', response_model = CreatorUser)
async def get_user(id:int, current_user= Depends(verify_token)):
        return await CreatorUserService.get_by_id(id)

@creator_user_router.get('/by_email/{email}', response_model = CreatorUser)
async def get_user(email:str, current_user = Depends(verify_token)):
        return await CreatorUserService.get_by_email(email)


@creator_user_router.delete("/delete/{user_id}")
async def user_create(user_id:int, current_user = Depends(verify_token)):
        await CreatorUserService.delete(id = user_id)
        return "200 OK"