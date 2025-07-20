from sqlalchemy import Column, String
from pgvector.sqlalchemy import Vector

from app.db.models.BaseModel import BaseModel


class UnicattLatestNews(BaseModel):

    __tablename__ = 'unicatt_latest_news'

    text = Column(String, nullable=True)
    embedding = Column(Vector(768), nullable=False)
    title = Column(String, nullable=False)
    pretitle = Column(String, nullable=True)

