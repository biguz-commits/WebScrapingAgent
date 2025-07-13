from sqlalchemy.orm import Session

from datetime import datetime

from app.db.models.UnicattLatestNews import UnicattLatestNews
from app.db.services.BaseUnicattService import BaseUnicattService


class UnicattService(BaseUnicattService):
    model = UnicattLatestNews

    def create(self, db: Session, **kwargs) -> UnicattLatestNews:
        obj = UnicattLatestNews(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get(self, db: Session, id: int) -> UnicattLatestNews | None:
        return db.query(UnicattLatestNews).filter(UnicattLatestNews.id == id).first()

    def list(self, db: Session, skip: int = 0, limit: int = 100, include_deleted: bool = False) -> list:
        return db.query(UnicattLatestNews).offset(skip).limit(limit).all()

    def update(self, db: Session, id: int, **kwargs) -> UnicattLatestNews | None:
        obj = db.query(UnicattLatestNews).filter(UnicattLatestNews.id == id).first()
        if not obj:
            return None
        for k, v in kwargs.items():
            setattr(obj, k, v)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: int) -> bool:
        obj = db.query(UnicattLatestNews).filter(UnicattLatestNews.id == id).first()
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True

    def soft_delete(self, db: Session, id: int) -> bool:
        obj = db.query(UnicattLatestNews).filter(UnicattLatestNews.id == id, UnicattLatestNews.deleted_at.is_(None)).first()
        if not obj:
            return False
        obj.deleted_at = datetime.now
        db.commit()
        return True