from tenji.request import RequestBase


class ShopRequest(RequestBase):
    def __init__(self, id: int) -> None:
        self.id = id

    def getPath(self) -> str:
        return f"{self.BASE_URL}shop/{self.id}"

    def getMethod(self):
        return "GET"
