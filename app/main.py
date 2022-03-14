from typing import List, Dict

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session  # type: ignore

from . import crud, models, schemas
from .database import engine
from .util import parse_sqlalchemy_query_output, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/items/", response_model=List[Dict])
def read_items(db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return parse_sqlalchemy_query_output(items)


@app.post("/create_item/", response_model=None)
def create_item(item: schemas.Item, db: Session = Depends(get_db)):
    crud.add_item(db, name=item.name, amount=item.amount_in_stock)


@app.post("/order_item", response_model=Dict)
def order_item(item: schemas.Item, db: Session = Depends(get_db)):
    return {
        "message": crud.remove_stock(db, name=item.name, amount=item.amount_in_stock)
    }
