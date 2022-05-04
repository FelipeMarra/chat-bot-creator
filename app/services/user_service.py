from fastapi import HTTPException, status

from sqlalchemy import delete
from sqlalchemy.future import select

from passlib.hash import bcrypt

from app.models.user_model import User
from app.db.connection import async_session

class UserService:
    async def create(name:str, email:str, password:str):
        async with async_session() as session:
            user = await UserService.get_by_email(email, False)

            if user:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with the email {email} already exists")

            hashed_password = bcrypt.hash(password)
            new_user = User(name=name, email=email, password=hashed_password)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

    async def get_by_id(id: int):
        async with async_session() as session:
            result = await session.execute(
                    select(User).where(User.id == id)
                )
            user = result.scalar()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with the id {id} dosen't exist")

        return user
    
    async def get_by_email(email:str, do_raise=True):
        async with async_session() as session:
            result = await session.execute(
                    select(User).where(User.email == email)
                )
            user = result.scalar()

        if not user and do_raise:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the email {email} dosen't exist")

        return user

    #TODO
    # async def update():
    #     async with async_session() as session:
    #         pass

    async def delete(id:int):
        async with async_session() as session:
            await session.execute(
                    delete(User).where(User.id == id)
                )
            await session.commit()
