from tenji.request import RequestBase


class HomeRequest(RequestBase):
    def __init__(self) -> None:
        pass

    def get_path(self) -> str:
        return self.BASE_URL

    def get_method(self):
        return "GET"
