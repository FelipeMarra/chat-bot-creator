from cgitb import reset
from sqlalchemy import delete
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.models.user_model import CreatorUser
from app.db.connection import async_session

class CreatorUserService:
    async def get_by_id(id: int):
        async with async_session() as session:
            result = await session.execute(select(CreatorUser).where(CreatorUser.id == id))
            user = result.scalar()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with the id {id} dosen't exist")

        return user
    
    async def get_by_email(email:str, do_raise=True):
        async with async_session() as session:
            result = await session.execute(select(CreatorUser).where(CreatorUser.email == email))
            user = result.scalar()

        if not user and do_raise:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the email {email} dosen't exist")

        return user

    async def create(name:str, email:str, password:str):
        async with async_session() as session:
            user = await CreatorUserService.get_by_email(email, False)

            if user:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with the email {email} already exists")

            new_user = CreatorUser(name=name, email=email, password=password)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

    async def delete(id:int):
        async with async_session() as session:
            await session.execute(delete(CreatorUser).where(CreatorUser.id == id))
            await session.commit()