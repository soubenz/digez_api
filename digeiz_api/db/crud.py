from sqlalchemy.orm import Session

from digeiz_api.db import models, schemas


def get_account(db: Session, account_id: int):
    return db.query(
        models.Account).filter(models.Account.id == account_id).first()


def get_account_by_name(db: Session, name: str):
    return db.query(models.Account).filter(models.Account.name == name).first()


def get_mall(db: Session, account_id: int):
    return db.query(
        models.Account).filter(models.Account.id == account_id).first()


def get_account_by_name(db: Session, name: str):
    return db.query(models.Account).filter(models.Account.name == name).first()


def create_account(db: Session,
                   account: schemas.AccountCreate,
                   mall: schemas.Mall = None):
    fake_hashed_password = account.password + "notreallyhashed"
    db_account = models.Account(name=account.name,
                                email=account.email,
                                hashed_password=fake_hashed_password,
                                mall=mall)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def create_mall(db: Session,
                mall: schemas.MallBase,
                units: [schemas.Unit] = []):
    db_mall = models.Mall(**mall.dict(), units=units)
    db.add(db_mall)
    db.commit()
    db.refresh(db_mall)
    return db_mall


def create_unit(db: Session, unit: schemas.UnitBase, mall_id: int = None):
    db_unit = models.Unit(**unit.dict(), mall_id=mall_id)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit
