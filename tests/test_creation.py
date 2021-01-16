import pytest
from digeiz_api.db import crud, models, schemas


def test_create_user(session):

    account = schemas.AccountCreate(name="test", email="test", password="aed")

    crud.create_account(session, account)
    assert session.query(models.Account).count() == 1


def test_create_mall(session):
    model = schemas.MallBase(name="My mall")
    crud.create_mall(session, model)
    assert session.query(models.Mall).count() == 1
    assert session.query(models.Mall).first().name == "My mall"


def test_create_unit(session):
    model = schemas.UnitBase(name="My unit")
    crud.create_unit(session, model)
    assert session.query(models.Unit).count() == 1
    assert session.query(models.Unit).first().name == "My unit"


def test_create_mall_account(session):
    mall = schemas.MallBase(name="My malfl")
    created_mall = crud.create_mall(session, mall)
    account = schemas.AccountCreate(name="test", email="test", password="aed")
    crud.create_account(session, account, created_mall)
    assert session.query(models.Mall).count() == 1
    assert session.query(models.Account).count() == 1
    assert session.query(models.Account).first().mall.id == 1


def test_create_mall_units(session, faker):
    mall = schemas.MallBase(name="My malfl")
    units = [
        crud.create_unit(session, schemas.UnitBase(name=faker.name()))
        for x in range(3)
    ]
    # print(units)
    crud.create_mall(session, mall, units)
    # assert session.query(models.Mall).count() == 1
    assert len(session.query(models.Mall).first().units) == 3
    # assert session.query(models.Mall).first().units) == 3


    # assert session.query(models.Account).count() == 1
    # assert session.query(models.Account).first().mall.id == 1
def test_create_unit_mall(session, faker):
    mall = schemas.MallBase(name="My mall")
    mall_c = crud.create_mall(session, mall)

    print(mall_c.name)
    unit_c = crud.create_unit(session,
                              schemas.UnitBase(name="unique"),
                              mall_id=mall_c.id)
    print(unit_c.mall.id)
    # print(units)
    # assert session.query(models.Unit).count() == 1
    assert session.query(models.Unit).filter(
        models.Unit.name == "unique").first().mall.name == "My mall"

    # assert session.query(models.Account).count() == 1
    # assert session.query(models.Account).first().mall.id == 1
