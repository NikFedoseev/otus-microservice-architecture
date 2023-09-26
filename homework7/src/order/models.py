from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON

from src.database.core import Base

class OrderModel(Base):
    __tablename__= 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())
    active = Column(Boolean, default=True)