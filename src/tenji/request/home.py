from tenji.request import RequestBase


class HomeRequest(RequestBase):
    def __init__(self) -> None:
        pass

    def getPath(self) -> str:
        return self.BASE_URL

    def getMethod(self):
        return "GET"
