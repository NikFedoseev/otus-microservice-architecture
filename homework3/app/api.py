from fastapi import APIRouter

from app.user.api import user_router


api_router = APIRouter(prefix='/api')

api_router.include_router(user_router, prefix='/user')

@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}