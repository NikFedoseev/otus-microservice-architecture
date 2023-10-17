import sqlalchemy as sa
from typing import Optional
from src.database.core import AsyncSession

from src.transaction.models import Transaction
from src.transaction.schemas import TransactionSchema
from src.transaction.exceptions import TransactionNotFound

async def add_transaction(
    db_session: AsyncSession,
    cart_id: int,
    operation: str,
    amount: float,
    created_by: int,
    order_id: Optional[int] = None,
):
    transaction = Transaction(
        cart_id=cart_id,
        order_id=order_id,
        operation=operation,
        amount=amount,
        created_by=created_by
    )

    db_session.add(transaction)
    await db_session.commit()

    return TransactionSchema.model_validate(transaction)


async def find_transaction_by_order_id(
    db_session: AsyncSession,
    order_id: int
) -> TransactionSchema:
    transaction = await db_session.scalar(
        sa.Select(Transaction).where(Transaction.order_id == order_id)
    )

    if not transaction:
        raise TransactionNotFound()

    return TransactionSchema.model_validate(transaction)


async def get_all_transactions(
    db_session: AsyncSession
):
    transactions = await db_session.scalars(
        sa.Select(Transaction)
    )

    return [
        TransactionSchema.model_validate(transaction)
        for transaction in transactions
    ]