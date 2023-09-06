from fastapi import APIRouter
from src.user.srv import router as auth_router

srv_router = APIRouter(prefix='/srv')

srv_router.include_router(auth_router, prefix='/auth')
