from fastapi import HTTPException, status

from sqlalchemy import delete, update
from sqlalchemy.future import select

from app.constants import CHATBOT_BASE_URL
from app.models import models
from app.schemas import states_schemas as schemas
from app.db.connection import async_session


class StateBaseService:
    async def create(state_model: models.StateBase, user: models.CreatorUser):
        async with async_session() as session:

            new_state = models.StateBase(
                name=state_model.name,
                chatbot_id=state_model.chatbot_id,
                state_type=state_model.state_type
            )

            session.add(new_state)
            await session.commit()
            await session.refresh(new_state)

            for message in state_model.messages:
                new_message = models.StateMessage(
                    message=message.message,
                    message_type=message.message_type,
                    state_id=new_state.id
                )
                session.add(new_message)

            # TODO Prevent creation of multiple transitions going to the same state
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

    async def update(state_id=id, update_data=schemas.StateBaseUpdate):
        async with async_session() as session:
            state_update = update(models.StateBase).where(
                models.StateBase.id == state_id)

            #update name
            if update_data.name:
                state_update = state_update.values(name=update_data.name)
            await session.execute(state_update)

            updated_state = await session.execute(
                select(models.StateBase).where(models.StateBase.id == state_id)
            )
            updated_state = updated_state.scalar()

            #update messages
            #TODO se tiver mensagem com o mesmo texto fudeu
            #TODO NAO ADICIONA NEM REMOVE, SÒ ATUALIZA OS QUE JA TEM 
            if update_data.messages:
                for message in update_data.messages:
                    message_update = update(models.StateMessage).where(
                                    models.StateMessage.id == message.id)
                    message_update = message_update.values(message=message.message)
                    
                    await session.execute(message_update)

            #update transitions
            #TODO NAO ADICIONA NEM REMOVE, SÒ ATUALIZA OS QUE JA TEM 
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
                delete(models.StateBase).where(models.StateBase.id == state_id)
            )
            await session.commit()

            return status.HTTP_200_OK
