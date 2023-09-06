from fastapi import APIRouter
from src.profile.api import router as profile_router

api_router = APIRouter(prefix='/api')

api_router.include_router(profile_router, prefix='/profile')

@api_router.get('/healthcheck', include_in_schema=False)
def healthcheck():
    return {'status': 'ok'}