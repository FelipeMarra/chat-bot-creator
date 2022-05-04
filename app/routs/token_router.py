from fastapi import  APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.services.token_service import authenticate_user, encode_user

token_router = APIRouter(prefix="/token", tags=["OAuth2 Token"])

@token_router.post("/")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    user_dict = {
        "id": user.id,
        "email": user.email,
        "password": user.password
    }
    
    encoded_jwt = encode_user(user_dict)

    return {"access_token": encoded_jwt, "token_type": "bearer"}