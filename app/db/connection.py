from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


DB_URL = getenv("DB_URL")

engine = create_async_engine(DB_URL)
async_session = sessionmaker(engine, class_=AsyncSession)