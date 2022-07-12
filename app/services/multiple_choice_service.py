from fastapi import HTTPException, status

from sqlalchemy import delete, update
from sqlalchemy.future import select

from app.constants import CHATBOT_BASE_URL
from app.models import models
from app.schemas import states_schemas as schemas
from app.db.connection import async_session


class MultipleChoiceService:
    async def create(multiple_choice_model: models.MultipleChoiceState, user: models.CreatorUser):
        async with async_session() as session:

            new_multiple_choice = models.MultipleChoiceState(
                name = multiple_choice_model.name,
                chatbot_id = multiple_choice_model.chatbot_id,
                min = multiple_choice_model.minSelectedChoices,
                max = multiple_choice_model.maxSelectedChoices,
                choices = multiple_choice_model.choices,
                decisions = multiple_choice_model.decisions                
            )

            session.add(new_multiple_choice)
            await session.commit()
            await session.refresh(new_multiple_choice)

            return new_multiple_choice

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
                select(models.MultipleChoiceState).where(models.MultipleChoiceState.id == state_id)
            )

            state = result.scalar()

            return state

    async def update(state_id=id, update_data=schemas.MultipleChoiceUpdate):
        async with async_session() as session:
            multiple_choice_update = update(models.MultipleChoiceState).where(
                models.MultipleChoiceState.id == state_id)

            #update name
            if update_data.name:
                multiple_choice_update = multiple_choice_update.values(name=update_data.name)
            await session.execute(multiple_choice_update)

            updated_multiple_choice = await session.execute(
                select(models.MultipleChoiceState).where(models.MultipleChoiceState.id == state_id)
            )
            updated_multiple_choice = updated_multiple_choice.scalar()

            #update min
            if update_data.minSelectedChoices:
                multiple_choice_update = multiple_choice_update.values(minSelectedChoices=update_data.minSelectedChoices)
            await session.execute(multiple_choice_update)

            updated_multiple_choice = await session.execute(
                select(models.MultipleChoiceState).where(models.MultipleChoiceState.id == state_id)
            )
            updated_multiple_choice = updated_multiple_choice.scalar()

            #update max   
            if update_data.maxSelectedChoices:
                multiple_choice_update = multiple_choice_update.values(maxSelectedChoices=update_data.maxSelectedChoices)
            await session.execute(multiple_choice_update)

            updated_multiple_choice = await session.execute(
                select(models.MultipleChoiceState).where(models.MultipleChoiceState.id == state_id)
            )
            updated_multiple_choice = updated_multiple_choice.scalar()

            #update choices  
            if update_data.choices:
                multiple_choice_update = multiple_choice_update.values(choices=update_data.choices)
            await session.execute(multiple_choice_update)

            updated_multiple_choice = await session.execute(
                select(models.MultipleChoiceState).where(models.MultipleChoiceState.id == state_id)
            )
            updated_multiple_choice = updated_multiple_choice.scalar()

            #update decisions  
            if update_data.decisions:
                multiple_choice_update = multiple_choice_update.values(decisions=update_data.decisions)
            await session.execute(multiple_choice_update)

            updated_multiple_choice = await session.execute(
                select(models.MultipleChoiceState).where(models.MultipleChoiceState.id == state_id)
            )
            updated_multiple_choice = updated_multiple_choice.scalar()
            
            await session.commit()


            return status.HTTP_200_OK

    async def delete(state_id: int):
        async with async_session() as session:
            await session.execute(
                delete(models.MultipleChoiceState).where(models.MultipleChoiceState.id == state_id)
            )
            await session.commit()

            return status.HTTP_200_OK
