from tenji.request.request_base import RequestBase

class BuyItemRequest(RequestBase):
    def __init__(self, id: int, jan: int = None, users: bool = False) -> None:
        self.id = id
        self.jan = jan
        self.users = users

    def get_path(self) -> str:
        return f"{self.BASE_URL}item/{self.id}"

    def get_method(self):
        return "POST"

    def get_params(self):
        p = {
            "commit": "loadWindow",
            "window": "buyItem",
            "soldBy": "users" if self.users else None,
            "jan": self.jan # used for user listings
        }
        return self.build_params(p)