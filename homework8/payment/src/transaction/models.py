from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from src.database.core import Base

class Transaction(Base):
    __tablename__= 'transaction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=True)
    operation = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    created_by = Column(Integer)