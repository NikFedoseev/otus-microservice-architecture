from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from src.database.core import Base

class UserModel(Base):
    __tablename__= 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    profile_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())
    active = Column(Boolean, default=True)