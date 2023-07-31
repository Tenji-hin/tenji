from typing import Optional
from pydantic import BaseModel

from tenji.model.item.item import Item
from tenji.model.paginated import Pagination


class Collection(BaseModel):
    items: list[Item] = []
    pagination: Optional[Pagination] = None
