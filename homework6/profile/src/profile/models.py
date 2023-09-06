from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date

from src.database.core import Base

class ProfileModel(Base):
    __tablename__= 'profile'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())