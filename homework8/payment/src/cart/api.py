from typing import List
from fastapi import APIRouter, Depends

from src.database.core import AsyncSession, get_db_session
from src.cart import use_cases as cart_use_cases
from src.cart.schemas import AddUserCartSchema, ReplenishCartSchema, UserCartOut

router = APIRouter()

@router.post('', response_model=UserCartOut)
async def add_cart(
    add_cart_in: AddUserCartSchema,
    db_session: AsyncSession = Depends(get_db_session),
):
    return await cart_use_cases.store_user_cart(
        db_session=db_session,
        user_id=add_cart_in.user_id,
        cart_number=add_cart_in.cart_number
    )


@router.get('', response_model=List[UserCartOut])
async def get_carts(
    db_session: AsyncSession = Depends(get_db_session),
):
    return await cart_use_cases.get_all_carts(
        db_session=db_session,
    )


@router.post('/{cart_id}/replenish', response_model=UserCartOut)
async def replenish_cart_by_id(
    cart_id: int,
    replenish_cart_in: ReplenishCartSchema,
    db_session: AsyncSession = Depends(get_db_session),
):
    return await cart_use_cases.replenish_cart(
        db_session=db_session,
        cart_id=cart_id,
        amount=replenish_cart_in.amount
    )