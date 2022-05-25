from fastapi import HTTPException, status

from sqlalchemy import delete, update
from sqlalchemy.future import select

from app.constants import CHATBOT_BASE_URL
from app.models import models
from app.schemas import chats_schemas as schemas
from app.db.connection import async_session


class StateBaseService:
    async def create(state_model: models.StateBase, user: models.CreatorUser):
        async with async_session() as session:

            # TODO Impedir criação de chatbot com mesmo nome

            new_state = models.StateBase(
                name=state_model.name,
                chatbot_id=state_model.chatbot_id
            )

            session.add(new_state)
            await session.commit()
            await session.refresh(new_state)

            for message in state_model.messages:
                new_message = models.StateMessage(
                    message=message.message,
                    type_message=message.type_message,
                    state_id=new_state.id
                )
                session.add(new_message)

            for transition in state_model.transitions:
                new_transition = models.StateTransition(
                    transition_to=transition.transition_to,
                    state_id=new_state.id
                )
                session.add(new_transition)

            await session.commit()
            await session.refresh(new_state)

            print(new_state.id)

            return new_state

    async def get_all(chat_id: int, user: models.CreatorUser):
        async with async_session() as session:
            result = await session.execute(
                select(models.ChatBot).where(
                    models.ChatBot.id == chat_id,
                )
            )

            chat_bot = result.scalar()

            return chat_bot.states


    async def get_by_id(state_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(models.StateBase).where(models.StateBase.id == state_id)
            )
    
            state = result.scalar()

            return state

    async def update(chatbot_id: int, update_data: schemas.ChatBotUpdate):
        async with async_session() as session:
            chat_update = update(models.ChatBot).where(
                models.ChatBot.id == chatbot_id)

            if update_data.name:
                chat_update = chat_update.values(name=update_data.name)
            if update_data.initial_state:
                chat_update = chat_update.values(
                    initial_state=update_data.initial_state)

            await session.execute(chat_update)
            await session.commit()

            updated_chatbot = await session.execute(
                select(models.ChatBot).where(models.ChatBot.id == chatbot_id)
            )
            updated_chatbot = updated_chatbot.scalar()

            return updated_chatbot

    async def delete(chatbot_id: int):
        async with async_session() as session:
            await session.execute(
                delete(models.ChatBot).where(models.ChatBot.id == chatbot_id)
            )
            await session.commit()
