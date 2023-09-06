from fastapi import FastAPI

from src.api import api_router
from src.srv import srv_router

app = FastAPI()

app.include_router(api_router)
app.include_router(srv_router)