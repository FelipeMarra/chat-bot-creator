from fastapi import HTTPException, status

from sqlalchemy import delete, update
from sqlalchemy.future import select

from app.constants import CHATBOT_BASE_URL
from app.models import models
from app.schemas import states_schemas as schemas
from app.db.connection import async_session


class OpenTextService:
    async def create(open_text_model: models.OpenTextState, user: models.CreatorUser):
        async with async_session() as session:

            #TODO add state base calling its creat function, and let it add messages and transitions

            new_open_text = models.OpenTextState(
                text = open_text_model.text,
                decisions = open_text_model.decisions            
            )

            session.add(new_open_text)
            await session.commit()
            await session.refresh(new_open_text)

            return new_open_text

    async def get_all(chat_id: int, user: models.CreatorUser):
        async with async_session() as session:
            result = await session.execute(
                select(models.ChatBot).where(
                    models.ChatBot.id == chat_id,
                )
            )

            chat_bot = result.scalar()

            #TODO fitler for state type
            return chat_bot.states

    async def get_by_id(state_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(models.OpenTextState).where(models.OpenTextState.id == state_id)
            )

            state = result.scalar()

            return state

    async def update(state_id=id, update_data=schemas.OpenTextUpdate):
        async with async_session() as session:
            open_text_update = update(models.OpenTextState).where(
                models.OpenTextState.id == state_id)

            #update text
            if update_data.text:
                open_text_update = open_text_update.values(name=update_data.name)
            await session.execute(open_text_update)

            updated_open_text = await session.execute(
                select(models.OpenTextState).where(models.OpenTextState.id == state_id)
            )
            updated_open_text = updated_open_text.scalar()

            #update decisions  
            if update_data.decisions:
                open_text_update = open_text_update.values(decisions=update_data.decisions)
            await session.execute(open_text_update)

            updated_open_text = await session.execute(
                select(models.OpenTextState).where(models.OpenTextState.id == state_id)
            )
            updated_open_text = updated_open_text.scalar()
            
            await session.commit()


            return status.HTTP_200_OK

    async def delete(state_id: int):
        async with async_session() as session:
            await session.execute(
                delete(models.OpenTextState).where(models.OpenTextState.id == state_id)
            )
            await session.commit()

            return status.HTTP_200_OK
