from tenji.request.request_base import RequestBase


class UserListsRequest(RequestBase):
    def __init__(self, username: str, page: int = 1) -> None:
        self.username = username
        self.page = page

    def get_path(self) -> str:
        return f"{self.BASE_URL}users.v4.php?mode=view&username={self.username}&tab=lists&page={self.page}"

    def get_method(self):
        return "GET"
