from typing import List, Optional
from pydantic import BaseModel

####################### States Base #########################
class StatesBaseBase(BaseModel):
    name: str
    messages: List[str] 
    transitions: List[int]

class StateBaseCreate(StatesBaseBase):
    chatbot_id: int

class StateBaseUpdate(StatesBaseBase):
    pass

class StateBase(StatesBaseBase):
    id: int
    chatbot_id: int

    class Config():
        orm_mode = True