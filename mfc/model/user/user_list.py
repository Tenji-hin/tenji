from typing import Optional
from pydantic import BaseModel

from mfc.model.item.item import Item
from mfc.model.paginated import Pagination


class UserList(BaseModel):
    id: int
    name: str
    owner: str
    icon: str
    created: str
    description: Optional[str] = None
    items: list[Item] = []
    tags: Optional[list[str]] = []
    pagination: Optional[Pagination] = None
