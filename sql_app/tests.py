import pytest
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

from . import crud, models
from .util import parse_sqlalchemy_query_output as parse


@pytest.fixture(scope="module", autouse=True)
def engine():
    engine = create_engine(
        "sqlite:///./test.db", connect_args={"check_same_thread": False}
    )
    models.Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="module", autouse=True)
def session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    yield SessionLocal()


def test_if_testdb_empty(session):
    assert parse(crud.get_items(session)) == []


def test_add_item(session):
    crud.add_item(session, "apple", 10)
    first_item_in_db = session.query(models.Item).first()
    assert first_item_in_db.name == "apple"
    assert first_item_in_db.amount_in_stock == 10


def test_remove_items(session):
    result_message = crud.remove_stock(session, "apple", 4)
    item_in_db = session.query(models.Item).first()
    assert item_in_db.name == "apple"
    assert item_in_db.amount_in_stock == 6
    assert result_message == "4 items ordered"


def test_remove_more_items_than_available(session):
    result_message = crud.remove_stock(session, "apple", 10)
    assert result_message == "6 items ordered"


def test_remove_nonexistent_items(session):
    result_message = crud.remove_stock(session, "orange", 4)
    assert result_message == "Item does not exist in the database"


def test_drop_table(engine):
    models.Base.metadata.drop_all(bind=engine)
