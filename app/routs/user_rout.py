from fastapi import APIRouter, Depends

from app.models.user_model import User
from app.services.user_service import UserService 
from app.schemas.user_schema import UserCreate, User
from app.services.token_service import decode_user

user_router = APIRouter(prefix="/user", tags=["Creator User"])

@user_router.post("/create", response_model = User)
async def user_create(user_input:UserCreate):
        return await UserService.create(name=user_input.name, email=user_input.email, password=user_input.password)

@user_router.get('/current', response_model = User)
async def get_user(current_user = Depends(decode_user)):
        return current_user

@user_router.get('/{id}', response_model = User)
async def get_user(id:int, current_user= Depends(decode_user)):
        return await UserService.get_by_id(id)

@user_router.get('/by_email/{email}', response_model = User)
async def get_user(email:str, current_user = Depends(decode_user)):
        return await UserService.get_by_email(email)


@user_router.delete("/delete/{user_id}")
async def user_create(user_id:int, current_user = Depends(decode_user)):
        await UserService.delete(id = user_id)
        return "200 OK"