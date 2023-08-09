
import json
from bs4 import BeautifulSoup


class MFCResponse:
    
    def __init__(self, body: str) -> None:
        self.body = body