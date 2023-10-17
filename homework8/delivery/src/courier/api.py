from typing import List
from fastapi import APIRouter, Depends

from src.database.core import AsyncSession, get_db_session
from src.courier import use_cases as courier_use_cases
from src.courier.schemas import CourierOut, BookedCourierSlotOutSchema

router = APIRouter()

@router.post('', response_model=CourierOut)
async def add_courier(
    db_session: AsyncSession = Depends(get_db_session),
):
    return await courier_use_cases.add_courier(
        db_session=db_session
    )


@router.get('', response_model=List[CourierOut])
async def get_all_couriers(
    db_session: AsyncSession = Depends(get_db_session),
):
    return await courier_use_cases.get_all_couriers(
        db_session=db_session
    )


@router.get('/{courier_id}/booked_slots', response_model=List[BookedCourierSlotOutSchema])
async def get_courier_booked_slots(
    courier_id: int,
    db_session: AsyncSession = Depends(get_db_session),
):
    return await courier_use_cases.get_courier_booked_slots(
        db_session=db_session,
        courier_id=courier_id
    )

# @router.post('/test')
# async def test_booking(
#     book_in: TestBook,
#     db_session: AsyncSession = Depends(get_db_session),
# ):
#     await courier_use_cases.book_courier(
#         db_session=db_session,
#         order_id=book_in.order_id,
#         order_created_at=book_in.order_created_at
#     )

