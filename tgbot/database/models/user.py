from sqlalchemy import Column, String, BigInteger, Integer

from tgbot.database.db_base import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    full_name = Column(String(length=80), nullable=False)
    username = Column(String(length=30), nullable=True)
    access = Column(Integer, default=0)
