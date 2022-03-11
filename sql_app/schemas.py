from pydantic import BaseModel


class Item(BaseModel):
    name: str
    amount_in_stock: int
