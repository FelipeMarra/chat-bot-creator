from sqlalchemy import Boolean, Column, Integer, String
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

#Representes the base to all states of the state machine. The other types specific properties will be defined according to the type propertie
class StateBase(Base):
    __tablename__ = "state_bases"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)

    name = Column(String)

    state_type = Column(String)

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
    message_type = Column(String)

    ############## Relationship State ###############
    state_id = Column(Integer, ForeignKey('state_bases.id'))
    state = relationship("StateBase", back_populates="messages", lazy='subquery')


class StateTransition(Base):
    __tablename__ = "states_transitions"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)

    transition_to = Column(Integer)

    ############## Relationship State ###############
    state_id = Column(Integer, ForeignKey('state_bases.id'))
    state = relationship("StateBase", back_populates="transitions", lazy='subquery')


#The properties that turns a base state into a single choice state - in other words: the coices.
class SingleChoiceState(Base):
    __tablename__ = "single_choice_state"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)

    #To refer to the state base from which this one derives
    state_base_id = Column(Integer, ForeignKey("state_bases.id"))

    ############## Relationship With Choices & Selected Choice###############
    #reference to a list of SingleChoiceChoice
    choices = relationship("SingleChoiceChoice", back_populates="state", lazy='subquery')

    #TODO https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html 
    #Nao funcionou usar forein key
    selected_id = Column(Integer)

#Represents a single choice from SingleChoiceState
class SingleChoiceChoice(Base):
    __tablename__ = "single_choice_choices"

    id = Column(Integer, primary_key=True, unique=True)

    #the choice's text that will be shown to the user
    description = Column(String)

    ############## Relationship With State ###############
    state_id = Column(Integer, ForeignKey('single_choice_state.id'))
    state = relationship("SingleChoiceState", back_populates="choices", lazy='subquery')

#The properties that turns a base state into a multiple choice state - in other words: the coices.
class MultipleChoiceState(Base):
    __tablename__ = "multiple_choice_state"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    minSelectedChoices = Column(Integer)
    maxSelectedChoices = Column(Integer)

    #To refer to the state base from which this one derives
    state_base_id = Column(Integer, ForeignKey("state_bases.id"))

    ############## Relationships ###############
    #reference to a list of MultipleChoiceChoice
    choices = relationship("MultipleChoiceChoice", back_populates="state", lazy='subquery')

    #reference to a list of MultipleChoiceDecision
    decisions = relationship("MultipleChoiceDecision", back_populates="state", lazy='subquery')

#Represents a multiple choice from MultipleChoiceState
class MultipleChoiceChoice(Base):
    __tablename__ = "multiple_choice_choice"

    id = Column(Integer, primary_key=True, unique=True)

    #the choice's text that will be shown to the user
    description = Column(String)

    category_id = Column(Integer, ForeignKey('multiple_choice_category.id'))

    is_selected = Column(Boolean)

    ############## Relationship With MultipleChoiceState ###############
    state_id = Column(Integer, ForeignKey('multiple_choice_state.id'))
    state = relationship("MultipleChoiceState", back_populates="choices", lazy='subquery')

class MultipleChoiceDecision(Base):
    __tablename__ = "multiple_choice_decision"
    
    id = Column(Integer, primary_key=True, unique=True)

    transition_id = Column(Integer, ForeignKey('state_bases.id'))

    category_id = Column(Integer, ForeignKey('multiple_choice_category.id'))

    ############## Relationship With MultipleChoiceState ###############
    state_id = Column(Integer, ForeignKey('multiple_choice_state.id'))
    state = relationship("MultipleChoiceState", back_populates="decisions", lazy='subquery')

class MultipleChoiceCategory(Base):
    __tablename__ = "multiple_choice_category"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)

    ##Open text state
class OpenTextState(Base):
    __tablename__ = "open_text_state"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    text = Column(String)

    #To refer to the state base from which this one derives
    state_base_id = Column(Integer, ForeignKey("state_bases.id"))

    #reference to a decision from open text state (?)
    decision = relationship("OpenTextDecision", back_populates="state", lazy='subquery')

    #Open text decision
class OpenTextDecision(Base):
    __tablename__ = "open_text_decision"
    
    id = Column(Integer, primary_key=True, unique=True)
    sentiment = Column(Integer) #integer for this number of the sentiment's detected on the table (?)
    grammarType = Column(Integer) #integer for this number of the grammar Type's detected on the table (?)

    transition_id = Column(Integer, ForeignKey('state_bases.id'))

    ############## Relationship With OpenTextState ###############
    state_id = Column(Integer, ForeignKey('open_text_state.id'))
    state = relationship("OpenTextState", back_populates="decision", lazy='subquery')
    