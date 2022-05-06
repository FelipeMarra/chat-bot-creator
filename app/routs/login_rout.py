from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.services import token_service

login_router = APIRouter(
    prefix="/login",
    tags=['Login']
)

@login_router.post('/')
async def loging(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await token_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password',
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=token_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token_service.create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )

    return {
        "name": user.name,
        "email": user.email,
        "id": user.id,
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds()),
    }