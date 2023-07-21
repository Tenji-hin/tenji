from mfc.request import RequestBase


class ProfileRequest(RequestBase):
    def __init__(self, username: str) -> None:
        self.username = username

    def getPath(self) -> str:
        return f"{self.BASE_URL}profile/{self.username}"
