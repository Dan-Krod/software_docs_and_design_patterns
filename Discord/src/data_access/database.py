from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from src.domain.models import Base

DATABASE_URL = "sqlite:///./data/database.sqlite"

class DatabaseSystem:
    def __init__(self, db_url: str = DATABASE_URL):
        self.engine = create_engine(
            db_url, connect_args={"check_same_thread": False}
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def create_tables(self):
        """Creates all 10+ tables based on SQLAlchemy models"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

    def test_connection(self) -> bool:
        """Implementation of testConnection() from UML"""
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

db_system = DatabaseSystem()