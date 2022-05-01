from fastapi import APIRouter, HTTPException 
from app.services.user_service import UserService 
from app.schemas.user_schema import UserCreate, User

user_router = APIRouter(prefix="/user", tags=["User"])

#TODO correct validation, try catch, wrong email answer, etc
@user_router.post("/create", response_model=User)
async def user_create(user_input:UserCreate):
        return await UserService.create(name=user_input.name, email=user_input.email, password=user_input.password)

#TODO correct validation, user deleting must be the user logged in
#try catch, wrong email answer, etc
@user_router.delete("/delete/{user_id}")
async def user_create(user_id:int):
        await UserService.delete(id=user_id)
        return "200 OK"