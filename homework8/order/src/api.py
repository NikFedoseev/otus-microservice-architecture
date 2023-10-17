from fastapi import APIRouter
from src.order.api import router as orders_router

api_router = APIRouter(prefix='/api')

api_router.include_router(orders_router, prefix='/orders')

@api_router.get('/healthcheck', include_in_schema=False)
def healthcheck():
    return {'status': 'ok'}