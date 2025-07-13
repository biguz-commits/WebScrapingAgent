from sqlalchemy.orm import Session
from datetime import datetime, timezone


class BaseUnicattService:
    model = None

    def create(self, db: Session, **kwargs):
        obj = self.model(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def list(self, db: Session, skip: int = 0, limit: int = 100, include_deleted: bool = False):
        query = db.query(self.model)
        if not include_deleted:
            query = query.filter(self.model.deleted_at.is_(None))
        return query.offset(skip).limit(limit).all()

    def update(self, db: Session, id: int, **kwargs):
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            return None
        for k, v in kwargs.items():
            setattr(obj, k, v)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: int):
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True

    def soft_delete(self, db: Session, id: int) -> bool:
        """Soft delete a record by setting deleted_at"""
        obj = db.query(self.model).filter(self.model.id == id, self.model.deleted_at.is_(None)).first()
        if not obj:
            return False
        obj.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
        db.commit()
        return True

    def restore(self, db: Session, id: int) -> bool:
        obj = db.query(self.model).filter(self.model.id == id, self.model.deleted_at.isnot(None)).first()
        if not obj:
            return False
        obj.deleted_at = None
        db.commit()
        return True