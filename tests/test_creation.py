import pytest
from digeiz_api.db import crud, models, schemas


def test_create_user(session):
    account = schemas.AccountCreate(name="test", email="test", password="aed")

    crud.create_account(session, account)
    assert len(crud.get_accounts(session)) == 1


def test_create_mall(session):
    model = schemas.MallBase(name="My mall")
    crud.create_mall(session, model)
    assert len(crud.get_malls(session)) == 1
    assert crud.get_mall_by_name(session, "My mall").name == model.name


def test_create_unit(session):
    model = schemas.UnitBase(name="My unit")
    crud.create_unit(session, model)
    assert len(crud.get_units(session)) == 1
    assert crud.get_unit_by_name(session, "My unit").name == model.name


def test_create_mall_account(session):
    mall = schemas.MallBase(name="My mall")
    created_mall = crud.create_mall(session, mall)
    account = schemas.AccountCreate(name="test", email="test", password="aed")
    crud.create_account(session, account, created_mall)
    assert len(crud.get_malls(session)) == 1
    assert len(crud.get_accounts(session)) == 1
    assert crud.get_account(session, 1).mall.id == 1


def test_create_mall_units(session, faker):
    mall = schemas.MallBase(name="My mall")
    units = [
        crud.create_unit(session, schemas.UnitBase(name=faker.name()))
        for x in range(3)
    ]
    crud.create_mall(session, mall, units)

    assert len(crud.get_mall(session, 1).units) == 3


def test_create_unit_mall(session, faker):
    mall = schemas.MallBase(name="My mall")
    mall_c = crud.create_mall(session, mall)
    crud.create_unit(session,
                     schemas.UnitBase(name="unique"),
                     mall_id=mall_c.id)
    assert crud.get_unit_by_name(session, "unique").mall.name == "My mall"


def test_pagination(session, faker):

    malls = [
        crud.create_mall(session, schemas.MallBase(name=faker.name()))
        for x in range(30)
    ]
    accounts = [
        crud.create_account(
            session,
            schemas.AccountCreate(name=faker.name(),
                                  email=faker.email(),
                                  password=faker.password()))
        for x in range(30)
    ]
    units = [
        crud.create_unit(session, schemas.UnitBase(name=faker.name()))
        for x in range(30)
    ]
    fetched_units = crud.get_units(session, skip=5, limit=4)
    assert len(fetched_units) == 4
    assert [unit.id for unit in fetched_units] == [x for x in range(6, 10)]
    fetched_accounts = crud.get_accounts(session, skip=10, limit=2)
    assert len(fetched_accounts) == 2
    assert [unit.id for unit in fetched_accounts] == [x for x in range(11, 13)]
    fetched_malls = crud.get_malls(session, skip=20, limit=5)
    assert len(fetched_malls) == 5
    assert [unit.id for unit in fetched_malls] == [x for x in range(21, 26)]
