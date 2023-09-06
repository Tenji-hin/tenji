from typing import Optional
from pydantic import BaseModel

from tenji.model.item.item import Item
from tenji.model.paginated import Pagination

class CollectionStats(BaseModel):
    owned: int = 0
    ordered: int = 0
    wished: int = 0

class Collection(BaseModel):
    items: list[Item] = []
    stats: Optional[CollectionStats] = None
    pagination: Optional[Pagination] = None
