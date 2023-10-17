from fastapi import APIRouter
from src.courier.api import router as products_router

api_router = APIRouter(prefix='/api')

api_router.include_router(products_router, prefix='/couriers')

@api_router.get('/healthcheck', include_in_schema=False)
def healthcheck():
    return {'status': 'ok'}