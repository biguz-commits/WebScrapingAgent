import os
import sqlalchemy
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import inspect
from app.db.models.UnicattLatestNews import UnicattLatestNews

from app.db.models.BaseModel import Base

load_dotenv()

class DbConnection:

    def __init__(
        self,
        host_name: str = os.getenv('POSTGRES_HOST'),
        database_name: str = os.getenv('POSTGRES_DB'),
        user_name: str = os.getenv('POSTGRES_USER'),
        password: str = os.getenv('POSTGRES_PASSWORD')
    ):
        self.host_name = host_name
        self.database_name = database_name
        self.user_name = user_name
        self.password = password

    def __url_object(self):
        return URL.create(
            "postgresql",
            username=self.user_name,
            password=self.password,
            host=self.host_name,
            database=self.database_name,
        )

    def create_engine(self):
        url = self.__url_object()
        engine = sqlalchemy.create_engine(url)
        return engine

    def create_session(self) -> Session:
        engine = self.create_engine()
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        try:
            yield SessionLocal
        finally:
            SessionLocal.close_all()

    def create_tables(self):
        engine = self.create_engine()
        Base.metadata.create_all(bind=engine)

    def langchain_db(self):
        connection_url = self.__url_object()
        db = SQLDatabase.from_uri(connection_url)
        return db


    @classmethod
    def db_init(cls):
        db = cls()
        engine = db.create_engine()
        inspector = inspect(engine)
        if inspector.has_table("unicatt_latest_news"):
            UnicattLatestNews.__table__.drop(engine)
            print("Dropped existing table.")

        Base.metadata.create_all(bind=engine)
        print("Created fresh tables.")
