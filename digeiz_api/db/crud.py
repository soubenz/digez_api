from sqlalchemy.orm import Session

from digeiz_api.db import models, schemas


def get_account(db: Session, account_id: int):
    return db.query(
        models.Account).filter(models.Account.id == account_id).first()


def get_account_by_name(db: Session, name: str):
    return db.query(models.Account).filter(models.Account.name == name).first()


def create_account(db: Session, account: schemas.AccountCreate):
    fake_hashed_password = account.password + "notreallyhashed"
    db_account = models.Account(name=account.name,email=account.email,
                          hashed_password=fake_hashed_password)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account
