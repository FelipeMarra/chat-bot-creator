from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CreatorUser(Base):
    __tablename__ = "creator_users"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    email = Column(String, primary_key=True, unique=True)
    password = Column(String)

    ############## Relationships ###############
    chat_bots = relationship("ChatBot", back_populates="creator_user", order_by="ChatBot.id", lazy='subquery')
    chats_historics = relationship("ChatHistoric", back_populates="creator_user", order_by="ChatHistoric.id", lazy='subquery')

class FinalUser(Base):
    __tablename__ = "final_users"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    cpf = Column(String)

    ############## Relationships ###############
    chats_historics = relationship("ChatHistoric", back_populates="final_user", order_by="ChatHistoric.id", lazy='subquery')

class ChatBot(Base):
    __tablename__ = "chat_bots"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    share_link = Column(String, unique=True)
    initial_state = Column(String)

    ############## Relationship With Creator User ###############
    creator_user_id = Column(Integer, ForeignKey('creator_users.id'))
    creator_user = relationship("CreatorUser", back_populates="chat_bots", lazy='subquery')

    #TODO
    ############## Relationship With States ###############
    #states = relationship("State", order_by="State.id")

class ChatHistoric(Base):
    __tablename__ = "chats_historics"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)
    share_link = Column(String, unique=True)
    initial_state = Column(String)

    ############## Relationship With Creator User ###############
    creator_user_id = Column(Integer, ForeignKey('creator_users.id'))
    creator_user = relationship("CreatorUser", back_populates="chats_historics", lazy='subquery')

    ############## Relationship With Final User ###############
    final_user_id = Column(Integer, ForeignKey('final_users.id'))
    final_user = relationship("FinalUser", back_populates="chats_historics", lazy='subquery')

    #TODO
    ############## Relationship With States ###############
    #states = relationship("State", order_by="State.id")