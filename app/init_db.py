from asyncio import run, set_event_loop_policy, WindowsSelectorEventLoopPolicy

from db.connection import engine
from models.user_model import Base

async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    
#start db
if __name__ == "__main__":
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    run(create_db())