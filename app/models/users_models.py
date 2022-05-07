from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.connection import Base

class CreatorUser(Base):
    __tablename__ = "creator_users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, primary_key=True, unique=True, index=True)
    password = Column(String)

    ############## Relationships ###############
    chat_bots = relationship("ChatBot", back_populates="creator_user", order_by="ChatBot.id")
    chats_historics = relationship("ChatHistoric", back_populates="creator_user", order_by="ChatHistoric.id")

class FinalUser(Base):
    __tablename__ = "final_users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    cpf = Column(String)

    ############## Relationships ###############
    chats_historics = relationship("ChatHistoric", back_populates="final_user", order_by="ChatHistoric.id")