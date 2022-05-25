from typing import List, Optional
from pydantic import BaseModel

####################### Message Base #########################


class MessageBase(BaseModel):
    message: str


class MessageCreate(MessageBase):
    type_message: str


class MessageUpdate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    state_id: int
    type_message: str

    class Config():
        orm_mode = True

####################### Trasition Base #########################
class TransitionBase(BaseModel):
    transition_to: int


class TransitionCreate(TransitionBase):
    pass

class TransitionUpdate(TransitionBase):
    pass


class Transition(TransitionBase):
    id: int
    state_id: int

    class Config():
        orm_mode = True



####################### States Base #########################
class StatesBaseBase(BaseModel):
    name: str


class StateBaseCreate(StatesBaseBase):
    chatbot_id: int
    messages: List[MessageCreate]
    transitions: List[TransitionCreate]

class StateBaseUpdate(StatesBaseBase):
    messages: List[MessageUpdate]
    transitions: List[TransitionUpdate]


class StateBase(StatesBaseBase):
    id: int
    chatbot_id: int
    messages: List[Message] = []
    transitions: List[Transition] = []

    class Config():
        orm_mode = True
