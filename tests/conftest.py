from digeiz_api.db import crud, models, schemas
from digeiz_api.db.connection import Session
from digeiz_api.api import app, get_db
from digeiz_api.db import crud
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def engine():
    SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./app_test.db"

    return create_engine(SQLALCHEMY_TEST_DATABASE_URL,
                         connect_args={"check_same_thread": False})


@pytest.fixture(scope="session")
def tables(engine):
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture
def session(engine, tables):
    """Returns an sqlalchemy session, and after the test tears 
    down everything properly."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def created_accounts(session, faker):
    return [
        crud.create_account(
            session,
            schemas.AccountCreate(name=faker.name(),
                                  email=faker.email(),
                                  password=faker.password()))
        for x in range(30)
    ]


@pytest.fixture
def created_malls(session, faker):
    return [
        crud.create_mall(session, schemas.MallBase(name=faker.name()))
        for x in range(2)
    ]


@pytest.fixture
def created_units(session, faker):
    return [
        crud.create_unit(session, schemas.UnitBase(name=faker.name()))
        for x in range(5)
    ]


def override_get_db(session):
    try:
        db = session
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    app.dependency_overrides[get_db] = lambda: session
    client = TestClient(app)
    return client
