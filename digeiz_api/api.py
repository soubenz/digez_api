from typing import List

import uvicorn
from fastapi import Body, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from digeiz_api.db import crud, models, schemas
from digeiz_api.db.connection import Session, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.post("/accounts/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate,
                   db: Session = Depends(get_db)):
    db_account = crud.get_account_by_name(db, name=account.name)
    print(db_account)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_account(db=db, account=account)


@app.get("/accounts/", response_model=List[schemas.Account])
def get_all_accounts(
        db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    db_accounts = crud.get_accounts(db, skip, limit)
    return db_accounts


@app.get("/accounts/{account_id}", response_model=schemas.Account)
def get_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@app.delete("/accounts/{account_id}", response_model=schemas.Removed)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.delete_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"entity": "account", "id": account_id}


@app.patch("/accounts/{account_id}", response_model=schemas.Modified)
def modify_account_name(account_id: int,
                        Body: schemas.ModifyName,
                        db: Session = Depends(get_db)):
    db_account = crud.modify_account_name(db, Body.name, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"entity": "account", "id": account_id}


@app.get("/malls/", response_model=List[schemas.Mall])
def get_all_malls(
        db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    db_malls = crud.get_malls(db, skip, limit)
    return db_malls


@app.get("/malls/{mall_id}", response_model=schemas.Mall)
def get_mall(mall_id: int, db: Session = Depends(get_db)):
    db_mall = crud.get_mall(db, mall_id=mall_id)
    if db_mall is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_mall


@app.delete("/malls/{mall_id}", response_model=schemas.Removed)
def delete_mall(mall_id: int, db: Session = Depends(get_db)):
    db_mall = crud.delete_mall(db, mall_id=mall_id)
    if db_mall is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"entity": "account", "id": mall_id}


@app.patch("/malls/{mall_id}", response_model=schemas.Modified)
def modify_mall_name(mall_id: int,
                     Body: schemas.ModifyName,
                     db: Session = Depends(get_db)):
    db_mall = crud.modify_mall_name(db, Body.name, mall_id=mall_id)
    if db_mall is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"entity": "account", "id": mall_id}


@app.post("/malls/", response_model=schemas.Mall)
def create_mall(mall: schemas.MallBase, db: Session = Depends(get_db)):
    db_mall = crud.get_mall_by_name(db, name=mall.name)
    if db_mall:
        raise HTTPException(status_code=400, detail="Mall already registered")
    return crud.create_mall(db=db, mall=mall)


@app.get("/units/", response_model=List[schemas.Unit])
def get_all_units(
        db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    db_units = crud.get_units(db, skip, limit)
    return db_units


@app.get("/units/{unit_id}", response_model=schemas.Unit)
def get_unit(unit_id: int, db: Session = Depends(get_db)):
    db_unit = crud.get_unit(db, unit_id=unit_id)
    if db_unit is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_unit


@app.delete("/units/{unit_id}", response_model=schemas.Removed)
def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    db_account = crud.delete_unit(db, unit_id=unit_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"entity": "account", "id": unit_id}


@app.patch("/units/{unit_id}", response_model=schemas.Modified)
def modify_unit_name(unit_id: int,
                     Body: schemas.ModifyName,
                     db: Session = Depends(get_db)):
    db_unit = crud.modify_unit_name(db, Body.name, unit_id=unit_id)
    if db_unit is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"entity": "account", "id": unit_id}


@app.post("/units/", response_model=schemas.Unit)
def create_unit(unit: schemas.UnitBase, db: Session = Depends(get_db)):
    db_unit = crud.get_unit_by_name(db, name=unit.name)
    if db_unit:
        raise HTTPException(status_code=400, detail="Unit already registered")
    return crud.create_unit(db=db, unit=unit)


def main():
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="debug")
