from typing import List, Optional
from pydantic import BaseModel

####################### Chat #########################
class ChatBotBase(BaseModel):
    name: str 
    share_link: str 
    initial_state: str
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
    #TODO
    #states: List[State]

class ChatHistoricCreate(ChatHistoricBase):
    pass

class ChatHistoric(ChatHistoricBase):
    id: int