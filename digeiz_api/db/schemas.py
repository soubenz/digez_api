from typing import List, Optional

from pydantic import BaseModel


class UnitBase(BaseModel):
    name: str
    is_active: bool = True


class Unit(BaseModel):
    id: int

    class Config:
        orm_mode = True


class MallBase(BaseModel):
    name: str
    is_active: bool = True


class Mall(MallBase):
    id: int
    units: List[Unit] = []

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    email: str
    name: str
    mall: Mall = None
    is_active: bool = True


class AccountCreate(AccountBase):
    password: str


class Account(AccountBase):
    id: int

    password: str

    # mall: Mall

    # items: List[Unit] = []

    class Config:
        orm_mode = True
