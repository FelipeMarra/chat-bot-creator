from typing import List, Optional
from pydantic import BaseModel
from app.schemas.chats_schemas import ChatBot, ChatHistoric

############### Creator User ################
class CreatorUserBase(BaseModel):
    name: str
    email: str

class CreatorUserCreate(CreatorUserBase):
    password: str

class CreatorUser(CreatorUserBase):
    id: int
    chats: List[ChatBot] = []
    chats_historics = List[ChatHistoric] = []

    class Config():
        orm_mode = True

############### Final User ################
class FinalUserBase(BaseModel):
    name: str
    email: Optional[str]
    phone: Optional[str]
    cpf: Optional[str]

class FinalUserCreate(FinalUserBase):
    pass

class FinalUser(FinalUserBase):
    id: int
    chats_historics = List[ChatHistoric] = []

    class Config():
        orm_mode = True