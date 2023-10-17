from typing import List
from fastapi import APIRouter, Depends

from src.database.core import AsyncSession, get_db_session
from src.products import use_cases as products_use_cases
from src.products.schemas import AddProductsShema, ProductOut

router = APIRouter()

@router.post('', response_model=List[ProductOut])
async def add_products(
    products_in: List[AddProductsShema],
    db_session: AsyncSession = Depends(get_db_session),
):
    return await products_use_cases.add_products(
        db_session=db_session,
        products_in=products_in
    )


@router.get('', response_model=List[ProductOut])
async def get_products(
    db_session: AsyncSession = Depends(get_db_session),
):
    return await products_use_cases.get_all_products(
        db_session=db_session
    )
