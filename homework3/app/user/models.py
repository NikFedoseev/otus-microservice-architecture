from sqlalchemy import Column, String, BigInteger

from app.database.core import Base

class UserModel(Base):
    __tablename__= 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(256))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)