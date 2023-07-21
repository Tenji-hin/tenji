from mfc.request import RequestBase


class ItemRequest(RequestBase):
    def __init__(self, id: int) -> None:
        self.id = id

    def getPath(self) -> str:
        return f"{self.BASE_URL}item/{self.id}"
