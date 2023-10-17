from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint
from src.database.core import Base

class Product(Base):
    __tablename__= 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, CheckConstraint("quantity >= 0", name="quantity_greater_then_zero"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())
