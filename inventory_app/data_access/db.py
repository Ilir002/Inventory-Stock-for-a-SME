from contextlib import contextmanager
from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine


# Pfad zur Datenbankdatei
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "inventory.db"
DB_URL = f"sqlite:///{DB_PATH}"


class Database:

    _engine = None

    @classmethod
    def engine(cls):
        if cls._engine is None:
            cls._engine = create_engine(DB_URL, echo=False)
        return cls._engine

    @classmethod
    def init(cls):
        # alle Tabellen aus models.py erstellen
        from inventory_app.domain.models import Category, Product, Order, OrderLine, Invoice  # noqa
        SQLModel.metadata.create_all(cls.engine())

    @classmethod
    @contextmanager
    def session(cls):
        # öffnet eine Verbindung zur DB und schliesst sie danach automatisch
        session = Session(cls.engine(), expire_on_commit=False)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()