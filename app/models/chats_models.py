from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.db.connection import Base

class ChatBot(Base):
    __tablename__ = "chat_bots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, primary_key=True, index=True)
    share_link: Column(String, unique=True) 
    initial_state: Column(String)

    ############## Relationship With Creator User ###############
    creator_user_id = Column(Integer, ForeignKey('creator_users.id'))
    creator_user = relationship("CreatorUser", back_populates="chat_bots")

    #TODO
    ############## Relationship With States ###############
    #states = relationship("State", order_by="State.id")

class ChatHistoric(Base):
    __tablename__ = "chats_historics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, primary_key=True, index=True)
    share_link: Column(String, unique=True) 
    initial_state: Column(String)

    ############## Relationship With Creator User ###############
    creator_user_id = Column(Integer, ForeignKey('creator_users.id'))
    creator_user = relationship("CreatorUser", back_populates="chats_historics")

    ############## Relationship With Final User ###############
    final_user_id = Column(Integer, ForeignKey('final_users.id'))
    final_user = relationship("FinalUser", back_populates="chats_historics")

    #TODO
    ############## Relationship With States ###############
    #states = relationship("State", order_by="State.id")

