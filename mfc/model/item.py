from pydantic import BaseModel

from mfc.model.category import ItemCategory


class Item(BaseModel):
    id: int
    name: str
    thumbnail: str
    category: ItemCategory
