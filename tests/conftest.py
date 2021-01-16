from digeiz_api.db import crud, models, schemas
from digeiz_api.db.connection import Session

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest


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