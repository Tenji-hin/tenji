from tenji.request.request_base import RequestBase

class BuyItemRequest(RequestBase):
    def __init__(self, id: int, jan: int = None, users: bool = False) -> None:
        self.id = id
        self.jan = jan
        self.users = users

    def getPath(self) -> str:
        return f"{self.BASE_URL}item/{self.id}"

    def getMethod(self):
        return "POST"

    def getParams(self):
        p = {
            "commit": "loadWindow",
            "window": "buyItem",
            "soldBy": "users" if self.users else None,
            "jan": self.jan # used for user listings
        }
        return self.build_params(p)