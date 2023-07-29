from pydantic import BaseModel


class UserListItem(BaseModel):
    id: int
    name: str
    owner: str
    icon: str
    created: str
    count: int = 0
