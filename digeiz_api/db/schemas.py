from typing import List, Optional

from pydantic import BaseModel


class Mall(BaseModel):
    id: int
    name: str
    is_active: bool

    # account_id: int
    # account: Account

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    email: str
    name: str


class AccountCreate(AccountBase):
    password: str


class Account(AccountBase):
    id: int
    is_active: bool
    password: str

    # mall: Mall

    # items: List[Unit] = []

    class Config:
        orm_mode = True


class Unit(BaseModel):
    id: int
    name: str
    is_active: bool

    # items: List[Item] = []

    class Config:
        orm_mode = True