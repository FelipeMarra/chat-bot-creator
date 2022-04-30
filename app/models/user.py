from app.db.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,  primary_key = True, autoincrement=True)
    email = Column(String)
    name = Column(String)