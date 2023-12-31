import datetime
from typing import Optional
from pydantic import BaseModel

from tenji.model.item.item import Item
from tenji.model.paginated import Pagination


class UserList(BaseModel):
    id: int
    name: str
    owner: str
    icon: str
    created: datetime.datetime
    description: Optional[str] = None
    items: list[Item] = []
    tags: Optional[list[str]] = []
    pagination: Optional[Pagination] = None
