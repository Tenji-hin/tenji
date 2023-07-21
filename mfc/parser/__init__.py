from bs4 import BeautifulSoup, Tag
import re


class ParserBase:
    def __init__(self, soup: BeautifulSoup) -> None:
        self._soup = soup

    def parse(self, **kwargs):
        raise NotImplementedError("Parser must implement a parse method")

    def try_get_text(self, selector: str, parent: Tag = None, default_value=None):
        p = parent if parent else self._soup

        node = p.select_one(selector) if selector else p
        if node:
            return node.text
        return default_value

    def try_get_list(self, selector: str, parent: Tag = None, default_value=None):
        text = self.try_get_text(selector, parent, default_value)
        if text:
            return text.split(",")
        return default_value

    def try_extract_number(self, text: str, default_value=None):
        text = text.replace(",", "")
        match = re.search(r"\d+", text)
        if match:
            return int(match.group(0))
        return default_value

    def try_get_style_background(self, style: str):
        match = re.search(r"url\((.+)\)", style)
        if match:
            return match.group(1)
        return None