from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint
from src.database.core import Base

class Courier(Base):
    __tablename__= 'courier'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())


class BookedCourierSlot(Base):
    __tablename__ = 'booked_courier_slot'

    courier_id = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False, primary_key=True)
    date_from = Column(DateTime, nullable=False)
    date_to = Column(DateTime, nullable=False)

