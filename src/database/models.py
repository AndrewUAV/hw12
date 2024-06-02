from sqlalchemy import Column, Integer, String, Date, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(50), nullable=False, index=True)
    email = Column(String(50), unique=True, index=True)
    phone_number = Column(String(15))
    birthday = Column(Date)
    additional_info = Column(Text)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column(
        'updated_at', DateTime, default=func.now(), onupdate=func.now()
    )
    user_id = Column(
        'user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None
    )
    user = relationship('User', backref="notes")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)