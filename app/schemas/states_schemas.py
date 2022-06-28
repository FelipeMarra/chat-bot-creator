from typing import List, Optional
from pydantic import BaseModel

####################### Message Base #########################
class MessageBase(BaseModel):
    message: str

class MessageCreate(MessageBase):
    message_type: str

class MessageUpdate(MessageBase):
    id: int

class Message(MessageBase):
    id: int
    state_id: int
    message_type: str

    class Config():
        orm_mode = True

####################### Trasition Base #########################
class TransitionBase(BaseModel):
    transition_to: int

class TransitionCreate(TransitionBase):
    pass

class TransitionUpdate(TransitionBase):
    id: int

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
    state_type: str
    messages: List[MessageCreate]
    transitions: List[TransitionCreate]

class StateBaseUpdate(StatesBaseBase):
    messages: List[MessageUpdate]
    transitions: List[TransitionUpdate]

class StateBase(StatesBaseBase):
    id: int
    state_type: str
    chatbot_id: int
    messages: List[Message] = []
    transitions: List[Transition] = []

    class Config():
        orm_mode = True

####################### Single Choice #########################
#state's choice
class SingleChoiceChoiceBase(BaseModel):
    description: str

class SingleChoiceChoiceCreate(SingleChoiceChoiceBase):
    state_id: int

class SingleChoiceChoiceUpdate(SingleChoiceChoiceBase):
    id: int

class SingleChoiceChoice(SingleChoiceChoiceBase):
    id: int
    state_id: int

    class Config():
        orm_mode = True

#state
class SingleChoiceBase(SingleChoiceChoiceBase):
    selected_id: int

class SingleChoiceCreate(SingleChoiceBase):
    state_base_id: int
    choices: List[SingleChoiceChoiceCreate]

class SingleChoiceUpdate(SingleChoiceBase):
    choices: List[SingleChoiceChoiceUpdate]

class SingleChoice(SingleChoiceBase):
    id: int
    state_base_id: int
    choices: List[SingleChoiceChoice] = []

    class Config():
        orm_mode = True


####################### Multiple Choice #########################
#state's choice
class MultipleChoiceChoiceBase(BaseModel):
    minSelectedChoices: int
    maxSelectedChoices: int
    selected_id: int
    description: str
    categoryChoice: int

class MultipleChoiceChoiceCreate(MultipleChoiceChoiceBase):
    state_base_id: int
    transition_id: int
    multiple_decision_id: int
    choice_decision_id: int
    category_id: int

class MultipleChoiceChoiceUpdate(MultipleChoiceChoiceBase):
    id: int

class MultipleChoiceChoice(MultipleChoiceChoiceBase):
    id: int
    state_base_id: int
    transition_id: int
    multiple_decision_id: int
    choice_decision_id: int
    category_id: int

    class Config():
        orm_mode = True

#state
class MultipleChoiceBase(MultipleChoiceChoiceBase):
    selected_id: int

class MultipleChoiceCreate(MultipleChoiceBase):
    state_base_id: int
    choices: List[MultipleChoiceChoiceCreate]

class MultipleChoiceUpdate(MultipleChoiceBase):
    choices: List[MultipleChoiceChoiceUpdate]

class MultipleChoice(MultipleChoiceBase):
    id: int
    state_base_id: int
    choices: List[MultipleChoiceChoice] = []

    class Config():
        orm_mode = True