from typing import List
from fastapi import APIRouter, Depends

from src.database.core import AsyncSession, get_db_session
from src.transaction import use_cases as transaction_use_cases
from src.transaction.schemas import TransactionSchema

router = APIRouter()

@router.get('', response_model=List[TransactionSchema])
async def get_all_transactions(
    db_session: AsyncSession = Depends(get_db_session)
):
    return await transaction_use_cases.get_all_transactions(
        db_session=db_session
    )
    