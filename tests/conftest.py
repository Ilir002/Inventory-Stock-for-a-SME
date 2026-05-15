import pytest
from sqlalchemy import event
from sqlmodel import SQLModel, Session, create_engine
import inventory_app.data_access.db as db_module


@pytest.fixture(autouse=True)
def isolated_database(monkeypatch):
    # für jeden Test -> leere DB
    test_engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(test_engine)
    monkeypatch.setattr(db_module.Database, "_engine", test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)