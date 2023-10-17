from datetime import datetime, timedelta
import sqlalchemy as sa
from src.database.core import AsyncSession

from src.courier.models import Courier, BookedCourierSlot
from src.courier.schemas import CourierSchema, BookedCourierSlotSchema
from src.courier.exceptions import HaveNotAvailableCouriers


async def get_all_couriers(
    db_session: AsyncSession
):
    couriers = await db_session.scalars(
        sa.Select(Courier)
    )

    return [CourierSchema.model_validate(courier) for courier in couriers]


async def add_courier(
    db_session: AsyncSession,
):
    courier = Courier()
    db_session.add(courier)

    await db_session.commit()

    return CourierSchema.model_validate(courier)


async def get_courier_booked_slots(
    db_session: AsyncSession,
    courier_id: int
):
    slots = await db_session.scalars(
        sa.Select(
            BookedCourierSlot
        ).where(
            BookedCourierSlot.courier_id == courier_id
        )
    )

    return [BookedCourierSlotSchema.model_validate(slot) for slot in slots]


async def book_courier(
    db_session: AsyncSession,
    order_id: int,
    order_created_at: datetime
) -> CourierSchema:
    
    stmt = sa.Select(Courier).outerjoin(
        BookedCourierSlot,
        Courier.id == BookedCourierSlot.courier_id,
    ).where(
        sa.or_(
            sa.not_(
                sa.Select(BookedCourierSlot)
                    .where(BookedCourierSlot.courier_id == Courier.id)
                    .exists()
                    .correlate(Courier)
            ),
            order_created_at > BookedCourierSlot.date_to
        )
    )
    
    courier = await db_session.scalar(
        stmt
    )

    if not courier:
        raise HaveNotAvailableCouriers
    
    booked_slot = BookedCourierSlot(
        courier_id=courier.id,
        order_id=order_id,
        date_from=order_created_at,
        date_to=order_created_at + timedelta(minutes=30)
    )

    db_session.add(booked_slot)
    await db_session.commit()

    return CourierSchema.model_validate(courier)
    
    
    