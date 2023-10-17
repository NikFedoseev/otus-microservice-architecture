from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from src.database.core import Base

class UserCart(Base):
    __tablename__= 'user_cart'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_number = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    money_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())