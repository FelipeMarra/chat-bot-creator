from app.models.user_model import User
from app.db.connection import async_session

class UserService:
    async def create_user(name:str, email:str, password:str):
        async with async_session() as session:
            new_user = User(name=name, email=email, password=password)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

