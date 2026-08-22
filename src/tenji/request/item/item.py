from tenji.request.request_base import RequestBase


class ItemRequest(RequestBase):
    def __init__(self, id: int) -> None:
        self.id = id

    def get_path(self) -> str:
        return f"{self.BASE_URL}item/{self.id}"

    def get_method(self):
        return "GET"
