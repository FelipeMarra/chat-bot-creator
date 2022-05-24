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
    chatbots = relationship("ChatBot", back_populates="creator_user", order_by="ChatBot.id", lazy='subquery')
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
    __tablename__ = "chatbots"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)

    name = Column(String)
    share_link = Column(String, unique=True)
    initial_state = Column(String)

    ############## Relationship With Creator User ###############
    creator_user_id = Column(Integer, ForeignKey('creator_users.id'))
    creator_user = relationship("CreatorUser", back_populates="chatbots", lazy='subquery')

    ############## Relationship With States ###############
    states = relationship("StateBase", back_populates="chatbot", order_by="StateBase.id", lazy='subquery')

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

class StateBase(Base):
    __tablename__ = "state_bases"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    
    name = Column(String)

    ############## Relationship With Chatbot ###############
    chatbot_id = Column(Integer, ForeignKey('chatbots.id'))
    chatbot = relationship("ChatBot", back_populates="states", lazy='subquery')

    ############## Relationships ###############
    messages = relationship("StateMessage", back_populates="state", order_by="StateMessage.id", lazy='subquery')
    transitions = relationship("StateTransition", back_populates="state", order_by="StateTransition.id", lazy='subquery')


class StateMessage(Base):
    __tablename__ = "states_messages"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    
    message = Column(String)
    type_message = Column(String)
    
    ############## Relationship State ###############
    state_id = Column(Integer, ForeignKey('state_bases.id'))
    state = relationship("StateBase", back_populates="messages", lazy='subquery')


class StateTransition(Base):
    __tablename__ = "states_transitions"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    
    transition_to = Column(Integer, unique = True)
    
    ############## Relationship State ###############
    state_id = Column(Integer, ForeignKey('state_bases.id'))
    state = relationship("StateBase", back_populates="transitions", lazy='subquery')
