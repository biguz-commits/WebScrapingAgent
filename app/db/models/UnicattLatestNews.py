from sqlalchemy import Column, String

from app.db.models.BaseModel import BaseModel


class UnicattLatestNews(BaseModel):

    __tablename__ = 'unicatt_latest_news'

    text = Column(String, nullable=True)
    title = Column(String, nullable=False)
    pretitle = Column(String, nullable=True)

