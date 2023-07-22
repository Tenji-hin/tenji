from mfc.request import RequestBase


class LoginRequest(RequestBase):
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def getPath(self) -> str:
        return f"{self.BASE_URL}sessions.v4.php"

    def getMethod(self):
        return "POST"

    def getParams(self):
        return {
            "username": self.username,
            "password": self.password,
            "commit": "signIn",
            "from": f"{self.BASE_URL}session/signin/",
        }
