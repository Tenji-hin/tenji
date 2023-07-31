from tenji.request.request_base import RequestBase


class UserListRequest(RequestBase):
    def __init__(self, id: int, page: int = 1) -> None:
        self.id = id
        self.page = page

    def getPath(self) -> str:
        return f"{self.BASE_URL}itemlists.v4.php?mode=view&itemListId={self.id}&tab=view&output=0&page={self.page}"

    def getMethod(self):
        return "GET"
