from fastapi import HTTPException, status

from sqlalchemy import delete, update
from sqlalchemy.future import select

from app.constants import CHATBOT_BASE_URL
from app.models import models
from app.schemas import chats_schemas as schemas
from app.db.connection import async_session


class ChatBotService:
    async def create(name: str, user: models.CreatorUser):
        async with async_session() as session:

            # TODO Impedir criação de chatbot com mesmo nome

            new_chatbot = models.ChatBot(name=name,
                                initial_state="",
                                creator_user_id=user.id,
                                share_link=f"{CHATBOT_BASE_URL}/{user.id}/{name}")

            session.add(new_chatbot)
            await session.commit()
            await session.refresh(new_chatbot)

            print(new_chatbot.id)

            return new_chatbot

    async def get_all(user: models.CreatorUser):
        async with async_session() as session:
            result = await session.execute(
                select(models.ChatBot).where(
                        models.ChatBot.creator_user_id == user.id
                    )
            )

            return result.scalars().all()

    async def get_by_id(chatbot_id:int):
        async with async_session() as session:
            chatbot = await session.execute(
                    select(models.ChatBot).where(models.ChatBot.id == chatbot_id)
                )
            chatbot = chatbot.scalar()

            return chatbot

    async def update(chatbot_id: int, update_data: schemas.ChatBotUpdate):
        async with async_session() as session:
            chat_update = update(models.ChatBot).where(models.ChatBot.id == chatbot_id)

            if update_data.name:
                chat_update = chat_update.values(name=update_data.name)
            if update_data.initial_state:
                chat_update = chat_update.values(initial_state=update_data.initial_state)

            await session.execute(chat_update)
            await session.commit()

            updated_chatbot = await session.execute(
                    select(models.ChatBot).where(models.ChatBot.id == chatbot_id)
                )
            updated_chatbot = updated_chatbot.scalar()

            return updated_chatbot

    async def delete(chatbot_id:int):
        async with async_session() as session:
            await session.execute(
                    delete(models.ChatBot).where(models.ChatBot.id == chatbot_id)
                )
            await session.commit()
