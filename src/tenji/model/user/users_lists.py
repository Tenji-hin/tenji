from pydantic import BaseModel
from tenji.model.paginated import Pagination

from tenji.model.user.user_list_item import UserListItem


class UserLists(BaseModel):
    items: list[UserListItem] = []
    pagination: Pagination = None
