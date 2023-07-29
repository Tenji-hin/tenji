from pydantic import BaseModel


class UserListBasic(BaseModel):
    id: int
    name: str
    owner: str
    icon: str
    created: str
    count: int = 0
