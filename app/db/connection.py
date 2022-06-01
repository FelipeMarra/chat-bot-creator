from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


#TODO get env
#onde ta postgres trocar por postgresql+asyncpg
DB_URL = "postgresql+asyncpg://taizrxoodcvrgv:4740ba87e57dcfede7b0809407b7ba5e0dce4bf606e6a7f55386077e33f3180e@ec2-54-204-56-171.compute-1.amazonaws.com:5432/d3tsq6h3ln3abb"
#DB_URL = getenv("DB_URL")

engine = create_async_engine(DB_URL)
async_session = sessionmaker(engine, expire_on_commit=False, future=True, class_=AsyncSession)