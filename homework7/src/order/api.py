from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.dependencies import get_idempotency_key
from src.database.core import get_db_session
from src.order import use_cases as order_use_cases
from src.order.schemas import CreateOrderSchema, OrderOutSchema, OrdersOutSchema
from src.order.exceptions import OrderConflict

router = APIRouter()

@router.post('', response_model=OrderOutSchema)
async def create_order(
    order_in: CreateOrderSchema,
    db_session: AsyncSession = Depends(get_db_session),
    idempotency_key: str = Depends(get_idempotency_key)
):  
    try:
        order = await order_use_cases.create_order(
            db_session=db_session,
            order_in=order_in,
            client_idempotency_key=idempotency_key
        )
    except OrderConflict:
        raise HTTPException(status_code=409, detail='mismatch client and server idempotency keys')
    
    return order


@router.get('', response_model=OrdersOutSchema)
async def get_orders(
    db_session: AsyncSession = Depends(get_db_session)
):
    orders = await order_use_cases.get_orders(db_session)
    idempotency_key = order_use_cases.get_idempotency_key(orders)

    return {
        "orders": orders,
        "idempotency_key": idempotency_key
    }
