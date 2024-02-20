from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.tables import Base


class Database:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

    def get_db(self):
        db = self.get_session()
        try:
            yield db
        finally:
            db.close()
