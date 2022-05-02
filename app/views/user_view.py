from fastapi import APIRouter, HTTPException
from app.models.user_model import CreatorUser 
from app.services.user_service import CreatorUserService 
from app.schemas.user_schema import CreatorUserCreate, CreatorUserCreate, CreatorUser

user_router = APIRouter(prefix="/user/creator", tags=["Creator User"])

#TODO correct validation, try catch, wrong email answer, etc
@user_router.post("/create", response_model=CreatorUser)
async def user_create(user_input:CreatorUserCreate):
        return await CreatorUserService.create(name=user_input.name, email=user_input.email, password=user_input.password)

@user_router.get('/{id}', response_model=CreatorUser)
async def get_user(id:int):
        return await CreatorUserService.get_by_id(id)

@user_router.get('/by_email/{email}')
async def get_user(email:str):
        return await CreatorUserService.get_by_email(email)

#TODO correct validation, user deleting must be the user logged in
#try catch, wrong email answer, etc
@user_router.delete("/delete/{user_id}")
async def user_create(user_id:int):
        await CreatorUserService.delete(id=user_id)
        return "200 OK"