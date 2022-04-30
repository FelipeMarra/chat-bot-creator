from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


#DB_URL = "postgresql+asyncpg://aoyjyqpilyfguy:bb7b2a0935f79cda7380a256cfae7668b44f89cc88a6e112b77438aeeba9c261@ec2-34-194-73-236.compute-1.amazonaws.com:5432/dpie2r7lfsq85"
DB_URL = getenv("DB_URL")

engine = create_async_engine(DB_URL)
async_session = sessionmaker(engine, class_=AsyncSession)