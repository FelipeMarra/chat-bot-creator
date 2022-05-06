from datetime import timedelta, datetime
from passlib.hash import bcrypt
from app.services.user_service import UserService
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
import jwt

SECRET_KEY = "4dbe73d09e99aabb258610f19dd5c696e05bd3dd12f34f930c1ac2cb345d5918"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

ACCESS_TOKEN_EXPIRE_MINUTES = 120

def create_access_token(data: dict, expires_delta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid email or password"
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
    return UserService.get_by_email(email)


async def verify_password(plain_password: str, hashed_password: str):
    return await bcrypt.verify(plain_password, hashed_password)

async def authenticate_user(email: str, password: str):
    user = await UserService.get_by_email(email)

    if not user or not verify_password(password, user.password):
        return False
    
    return user
