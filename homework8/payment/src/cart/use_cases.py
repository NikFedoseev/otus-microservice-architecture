
import sqlalchemy as sa
from typing import Optional
from src.database.core import AsyncSession

from src.cart.models import UserCart
from src.cart.exceptions import CartNotFound, UnknownOperation, NotEnoughMoney
from src.cart.constants import CartOperation
from src.cart.schemas import UserCartOut
from src.transaction.use_cases import add_transaction, find_transaction_by_order_id
from src.transaction.exceptions import TransactionNotFound


async def get_all_carts(
    db_session: AsyncSession
):
    carts = await db_session.scalars(
        sa.Select(UserCart)
    )

    return [UserCartOut.model_validate(cart) for cart in carts]


async def find_cart_by(
    db_session: AsyncSession,
    cart_number: Optional[str] = None,
    cart_id: Optional[int] = None
) -> UserCart:
    stmt = sa.Select(UserCart)

    if cart_number:
        stmt = stmt.where(
            UserCart.cart_number == cart_number
        )

    if cart_id:
        stmt = stmt.where(
            UserCart.id == cart_id
        )
   
    
    cart = await db_session.scalar(stmt)

    if not cart:
        raise CartNotFound
    
    return cart


async def store_user_cart(
    db_session: AsyncSession,
    user_id: int,
    cart_number: str
):
    user_cart = UserCart(
        user_id=user_id, 
        cart_number=cart_number, 
        money_amount=0
    )

    db_session.add(user_cart)
    await db_session.commit()

    return user_cart


async def replenish_cart(
    db_session: AsyncSession,
    cart_id: int,
    amount: float
):
    cart = await find_cart_by(
        db_session=db_session,
        cart_id=cart_id
    )
    
    cart.money_amount += amount

    await add_transaction(
        db_session=db_session,
        cart_id=cart.id,
        operation=CartOperation.REPLENISHMENT.value,
        created_by=1,
        amount=amount
    )

    await db_session.commit()

    return cart


async def refund_money_by_cart_transaction(
    db_session: AsyncSession,
    order_id: int,
):
    try:
        transaction = await find_transaction_by_order_id(
            db_session=db_session,
            order_id=order_id
        )
    except TransactionNotFound:
        return

    cart = await find_cart_by(
        db_session=db_session,
        cart_id=transaction.cart_id
    )

    cart.money_amount += transaction.amount

    await add_transaction(
        db_session=db_session,
        cart_id=transaction.cart_id,
        operation=CartOperation.REFUNDING.value,
        created_by=1,
        order_id=transaction.order_id,
        amount=transaction.amount
    )

    await db_session.commit()


async def pay_order(
    db_session: AsyncSession,
    order_id: int,
    price: float,
    cart_number: str,
    user_id: int
):
    transaction = None

    try:
        transaction = await find_transaction_by_order_id(
            db_session=db_session,
            order_id=order_id
        )
    except TransactionNotFound as e:
        print(e, "EXC1")
    except Exception as e:
        print(e, "EXC2")
    
    if transaction and transaction.operation == CartOperation.DEBITING.value:
        return

    cart = await find_cart_by(
        db_session=db_session,
        cart_number=cart_number
    )
    
    if cart.money_amount < price:
        raise NotEnoughMoney
    
    cart.money_amount -= price

    t = await add_transaction(
        db_session=db_session,
        cart_id=cart.id,
        operation=CartOperation.DEBITING.value,
        amount=price,
        created_by=user_id,
        order_id=order_id
    )

    print(t)
    await db_session.commit()
