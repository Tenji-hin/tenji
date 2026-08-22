from tenji.model.user.collectionstatus import CollectionStatus
from tenji.request.request_base import RequestBase


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

    def get_path(self) -> str:
        # the raw value, as formatting the enum yields its name on Python 3.11+
        status = getattr(self.status, "value", self.status)
        return f"{self.BASE_URL}users.v4.php?mode=view&username={self.username}&tab=collection&page={self.page}&status={status}&output=0"

    def get_method(self):
        return "GET"
