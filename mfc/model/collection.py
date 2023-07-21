from pydantic import BaseModel

from mfc.model.item import Item


class Collection(BaseModel):
    items: list[Item] = []
