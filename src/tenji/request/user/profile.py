from tenji.request.request_base import RequestBase


class ProfileRequest(RequestBase):
    def __init__(self, username: str) -> None:
        self.username = username

    def get_path(self) -> str:
        return f"{self.BASE_URL}profile/{self.username}"

    def get_method(self):
        return "GET"
