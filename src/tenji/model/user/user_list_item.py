import datetime
from pydantic import BaseModel


class UserListItem(BaseModel):
    id: int
    name: str
    owner: str
    icon: str
    created: datetime.datetime
    count: int = 0
