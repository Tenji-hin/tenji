from pydantic import BaseModel
from mfc.model.user_list import UserList
from mfc.model.user_list_basic import UserListBasic


class UserLists(BaseModel):
    items: list[UserListBasic] = []
