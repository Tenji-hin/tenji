from tenji.request.request_base import RequestBase


class ShopRequest(RequestBase):
    def __init__(self, id: int) -> None:
        self.id = id

    def get_path(self) -> str:
        return f"{self.BASE_URL}shop/{self.id}"

    def get_method(self):
        return "GET"
