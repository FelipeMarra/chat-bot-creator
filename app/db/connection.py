from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

#TODO get env
DB_URL = "postgresql+asyncpg://rfjpmayqxkhcqo:bafd6597046b8068832c55ae56b253acbd3af8155c0bbe19e1ce6ce161f2cdb0@ec2-54-204-56-171.compute-1.amazonaws.com:5432/d9don60opg8pec"
#DB_URL = getenv("DB_URL")

engine = create_async_engine(DB_URL)
async_session = sessionmaker(engine, expire_on_commit=False, future=True, class_=AsyncSession)
Base = declarative_base()