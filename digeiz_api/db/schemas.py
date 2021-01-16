from typing import List, Optional

from pydantic import BaseModel


class UnitBase(BaseModel):
    name: str


class Unit(BaseModel):
    id: int
    is_active: bool = True

    # items: List[Item] = []
    class Config:
        orm_mode = True


class MallBase(BaseModel):
    name: str


class Mall(MallBase):
    id: int
    is_active: bool = True

    units: List[Unit] = []

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    email: str
    name: str
    mall: Mall = None


class AccountCreate(AccountBase):
    password: str


class Account(AccountBase):
    id: int
    is_active: bool = True
    password: str

    # mall: Mall

    # items: List[Unit] = []

    class Config:
        orm_mode = True
