from pydantic import BaseModel

from mfc.model.user.user_list_item import UserListItem



class UserLists(BaseModel):
    items: list[UserListItem] = []
