from typing import List, Optional
from pydantic import BaseModel
from app.schemas.users_schemas import CreatorUser, FinalUser

####################### Chat #########################
class ChatBotBase(BaseModel):
    name: str 
    share_link: str 
    initial_state: str
    creator_user: CreatorUser
    #TODO
    #states: List[State]

class ChatBotCreate(ChatBotBase):
    pass

class ChatBot(ChatBotBase):
    id: int   

####################### Chat Historic#########################
class ChatHistoricBase(BaseModel):
    name: str
    share_link: str
    creator_user: CreatorUser
    fina_user: FinalUser
    #TODO
    #states: List[State]

class ChatHistoricCreate(ChatHistoricBase):
    pass

class ChatHistoric(ChatHistoricBase):
    id: int