from fastapi import APIRouter, HTTPException 
from app.services.user_service import UserService 
from app.schemas.user_schema import UserCreate, User

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.post("/create", response_model=User)
async def user_create(user_input:UserCreate):
        return await UserService.create_user(name=user_input.name, email=user_input.email, password=user_input.password)