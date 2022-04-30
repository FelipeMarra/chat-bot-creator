from asyncio import run, set_event_loop_policy, WindowsSelectorEventLoopPolicy

from connection import engine
from base import Base

async def create_db():
    async with engine.begin() as connection:
        print("2")
        await connection.run_sync(Base.metadata.drop_all)
        print("3")
        await connection.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    #set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    print("1")
    run(create_db())
    print("4")
