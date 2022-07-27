from fastapi import HTTPException, status

from sqlalchemy import delete, update
from sqlalchemy.future import select

from app.constants import CHATBOT_BASE_URL
from app.models import models
from app.schemas import states_schemas as schemas
from app.db.connection import async_session


class SingleChoiceService:
    async def create(single_choice_model: models.SingleChoiceState, user: models.CreatorUser):
        async with async_session() as session:

            #TODO add state base calling its creat function, and let it add messages and transitions

            new_single_choice = models.SingleChoiceState(
                name=single_choice_model.name,
                chatbot_id=single_choice_model.chatbot_id,
                choice=single_choice_model.choice                
            )

            session.add(new_single_choice)
            await session.commit()
            await session.refresh(new_single_choice)

            for message in single_choice_model.messages:
                new_message = models.StateMessage(
                    message=message.message,
                    message_type=message.message_type,
                    state_id=new_single_choice.id
                )
                session.add(new_message)

            for transition in single_choice_model.transitions:
                new_transition = models.StateTransition(
                    transition_to=transition.transition_to,
                    state_id=new_single_choice.id
                )
                session.add(new_transition)

            await session.commit()
            await session.refresh(new_single_choice)

            print(new_single_choice.id)

            return new_single_choice

    async def get_all(chat_id: int, user: models.CreatorUser):
        async with async_session() as session:
            result = await session.execute(
                #TODO filter multiple choice states
                select(models.ChatBot).where(
                    models.ChatBot.id == chat_id,
                )
            )

            chat_bot = result.scalar()

            return chat_bot.states

    async def get_by_id(state_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(models.SingleChoiceState).where(models.SingleChoiceState.id == state_id)
            )

            state = result.scalar()

            return state

    async def update(state_id=id, update_data=schemas.SingleChoiceUpdate):
        async with async_session() as session:
            single_choice_update = update(models.SingleChoiceState).where(
                models.SingleChoiceState.id == state_id)

            #update name
            if update_data.name:
                single_choice_update = single_choice_update.values(name=update_data.name)
            await session.execute(single_choice_update)

            updated_single_choice = await session.execute(
                select(models.SingleChoiceState).where(models.SingleChoiceState.id == state_id)
            )
            updated_single_choice = updated_single_choice.scalar()

            #update messages
            #TODO se tiver mensagem com o mesmo texto fudeu
            if update_data.messages:
                for message in update_data.messages:
                    message_update = update(models.StateMessage).where(
                                    models.StateMessage.id == message.id)
                    message_update = message_update.values(message=message.message)
                    
                    await session.execute(message_update)

            #update transitions
            if update_data.transitions:
                for transition in update_data.transitions:                 
                    transition_update = update(models.StateTransition).where(
                                    models.StateTransition.id == transition.id)
                    transition_update = transition_update.values(transition_to=transition.transition_to)
                    
                    await session.execute(transition_update)

            await session.commit()


            return status.HTTP_200_OK

    async def delete(state_id: int):
        async with async_session() as session:
            await session.execute(
                delete(models.SingleChoiceState).where(models.SingleChoiceState.id == state_id)
            )
            await session.commit()

            return status.HTTP_200_OK
