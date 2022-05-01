from sqlalchemy import delete
from app.models.user_model import User
from app.db.connection import async_session

class UserService:
    async def create(name:str, email:str, password:str):
        async with async_session() as session:
            new_user = User(name=name, email=email, password=password)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

    async def delete(id:int):
        async with async_session() as session:
            await session.execute(delete(User).where(User.id == id))
            await session.commit()
