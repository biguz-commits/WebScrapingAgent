from dotenv import load_dotenv
from sqlalchemy import inspect

from app.db.DbConnection import DbConnection
import os

from app.db.models.BaseModel import Base
from app.db.models.UnicattLatestNews import UnicattLatestNews

load_dotenv()


def main():
    host_name = os.getenv('POSTGRES_HOST')
    user = os.getenv('POSTGRES_USER')
    db_name = os.getenv('POSTGRES_DB')
    password = os.getenv('POSTGRES_PASSWORD')
    db = DbConnection(host_name=host_name, database_name=db_name,
                      user_name=user, password=password)

    print(db.url_object())



def reset_tables():
    host_name = os.getenv('POSTGRES_HOST')
    user = os.getenv('POSTGRES_USER')
    db_name = os.getenv('POSTGRES_DB')
    password = os.getenv('POSTGRES_PASSWORD')
    db = DbConnection(host_name=host_name, database_name=db_name,
                      user_name=user, password=password)
    engine = db.create_engine()
    inspector = inspect(engine)
    if inspector.has_table("unicatt_latest_news"):
        UnicattLatestNews.__table__.drop(engine)
        print("Dropped existing table.")

    Base.metadata.create_all(bind=engine)
    print("Created fresh tables.")

#if __name__ == "__main__":
    #reset_tables()


if __name__ == '__main__':
    main()
