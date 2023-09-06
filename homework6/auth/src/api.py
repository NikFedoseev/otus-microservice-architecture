from fastapi import APIRouter
from src.user.api import router as auth_router

api_router = APIRouter(prefix='/api')

api_router.include_router(auth_router, prefix='/auth')

@api_router.get('/healthcheck', include_in_schema=False)
def healthcheck():
    return {'status': 'ok'}