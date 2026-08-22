from bs4 import BeautifulSoup


class MFCResponse:

    def __init__(self, body: str) -> None:
        self.body = body
        self._soup = None

    @property
    def soup(self) -> BeautifulSoup:
        """The response body parsed as HTML, built on first access"""
        if self._soup is None:
            self._soup = BeautifulSoup(self.body, "html.parser")
        return self._soup
