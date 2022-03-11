from sqlalchemy.orm import Session  # type: ignore

from . import models


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def remove_stock(db: Session, name: str, amount: int):
    current_object = db.query(models.Item).filter_by(name=name).first()
    if current_object is not None:
        setattr(
            current_object,
            "amount_in_stock",
            max(0, current_object.amount_in_stock - amount),
        )
        db.commit()
        return f"{min(amount, current_object.amount_in_stock)} items ordered"
    else:
        return "Item does not exist in the database"


def add_item(db: Session, name: str, amount: int):
    current_object = db.query(models.Item).filter_by(name=name).first()
    if current_object is not None:
        setattr(
            current_object, "amount_in_stock", current_object.amount_in_stock + amount
        )
        db.commit()
    else:
        db_item = models.Item(name=name, amount_in_stock=amount)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
