from fastapi import APIRouter
from src.profile.srv import router as profile_router

srv_router = APIRouter(prefix='/srv')

srv_router.include_router(profile_router, prefix='/profile')
