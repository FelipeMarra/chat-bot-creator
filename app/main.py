from fastapi import FastAPI
from app.views.user_view import user_router

#start app
app = FastAPI()

#add routs
app.include_router(user_router)