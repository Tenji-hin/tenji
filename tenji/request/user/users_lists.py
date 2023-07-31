from tenji.request.request_base import RequestBase


class UserListsRequest(RequestBase):
    def __init__(self, username: str) -> None:
        self.username = username

    def getPath(self) -> str:
        return f"{self.BASE_URL}profile/{self.username}/lists/"

    def getMethod(self):
        return "GET"
