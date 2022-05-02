from typing import List, Optional
from pydantic import BaseModel

############### A Generic User ################
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config():
        orm_mode = True

############# A Creator User, extends the generic one ################
#creator user is the one that is able to create chatbots
class CreatorUserBase(UserBase):
    pass

class CreatorUserCreate(UserCreate):
    pass

class CreatorUser(User):
    pass

