from pydantic import BaseModel

from tenji.model.user.user_list_item import UserListItem


class UserLists(BaseModel):
    items: list[UserListItem] = []
