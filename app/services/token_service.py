from passlib.hash import bcrypt
from app.services.user_service import UserService
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
import jwt

SECRET_KEY = "4dbe73d09e99aabb258610f19dd5c696e05bd3dd12f34f930c1ac2cb345d5918"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def encode_user(user_dict):
    return jwt.encode(user_dict, SECRET_KEY, algorithm=ALGORITHM)

async def decode_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = await UserService.get_by_id(payload.get("id")) 
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )

    return user

async def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.verify(plain_password, hashed_password)

async def authenticate_user(email: str, password: str):
    user = await UserService.get_by_email(email)

    if not user or not verify_password(password, user.password):
        return False
    
    return user