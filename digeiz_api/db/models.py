from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

from digeiz_api.db.connection import Base


class Mall(Base):
    __tablename__ = "malls"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    units = relationship("Unit", backref="mall")
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship("Account", back_populates="mall")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    mall = relationship("Mall", uselist=False, back_populates="account")


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    mall_id = Column(Integer, ForeignKey('malls.id'))
    # mall = relationship("Mall")
