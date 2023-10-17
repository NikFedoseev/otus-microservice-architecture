from fastapi import APIRouter
from src.cart.api import router as carts_router
from src.transaction.api import router as transactions_router

api_router = APIRouter(prefix='/api')

api_router.include_router(carts_router, prefix='/carts')
api_router.include_router(transactions_router, prefix='/transactions')

@api_router.get('/healthcheck', include_in_schema=False)
def healthcheck():
    return {'status': 'ok'}