from enum import Enum
from mfc.request import RequestBase


class CollectionStatus(str, Enum):
    Wished = 0
    Ordered = 1
    Owned = 2
    Favorites = 3


class CollectionRequest(RequestBase):
    def __init__(
        self,
        username: str,
        status: CollectionStatus,
        page: int = 1,
    ) -> None:
        self.username = username
        self.status = status
        self.page = page

    def getPath(self) -> str:
        return f"{self.BASE_URL}users.v4.php?mode=view&username={self.username}&tab=collection&page={self.page}&status={self.status}&output=0"
