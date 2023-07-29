from typing import Optional
from pydantic import BaseModel

from mfc.model.item.item import Item
from mfc.model.paginated import Pagination


class Collection(BaseModel):
    items: list[Item] = []
    pagination: Optional[Pagination] = None
