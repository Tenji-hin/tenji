from tenji.request import RequestBase


class LoginRequest(RequestBase):
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def get_path(self) -> str:
        return f"{self.BASE_URL}sessions.v4.php"

    def get_method(self):
        return "POST"

    def get_params(self):
        return {
            "username": self.username,
            "password": self.password,
            "commit": "signIn",
            "from": f"{self.BASE_URL}session/signin/",
        }
