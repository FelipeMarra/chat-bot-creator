from typing import List
from pydantic import BaseModel

from app.schemas.states_schemas import StateBase

####################### Chat #########################
class ChatBotBase(BaseModel):
    name: str 

class ChatBotCreate(ChatBotBase):
    pass

class ChatBotUpdate(ChatBotBase):
    initial_state: str

class ChatBot(ChatBotBase):
    id: int
    creator_user_id: int
    share_link: str
    initial_state: str
    states: List[StateBase] = []

    class Config():
        orm_mode = True

####################### Chat Historic#########################
class ChatHistoricBase(BaseModel):
    name: str
    share_link: str
    creator_user_id: int
    final_user_id: int
    #TODO
    #states: List[State]
    

class ChatHistoricCreate(ChatHistoricBase):
    pass

class ChatHistoric(ChatHistoricBase):
    id: int

    class Config():
        orm_mode = True