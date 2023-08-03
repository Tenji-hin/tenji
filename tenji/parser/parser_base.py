import datetime
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse
from urllib.parse import parse_qs


import re

from tenji.model.paginated import Pagination


class ParserBase:
    def __init__(self, soup: BeautifulSoup) -> None:
        self._soup = soup

    def parse(
        self,
        selector: str,
        parent: Tag = None,
    ):
        p = parent if parent else self._soup
        node = p.select_one(selector) if selector else p
        return node

    def try_get_tag(
        self,
        selector: str,
        parent: Tag = None,
    ):
        p = parent if parent else self._soup
        node = p.select_one(selector) if selector else p
        return node

    def try_get_text(self, selector: str, parent: Tag = None, default_value=None):
        node = self.try_get_tag(selector, parent)
        if node:
            return node.text
        return default_value

    def try_get_value(
        self, selector: str, attr: str, parent: Tag = None, default_value=None
    ):
        node = self.try_get_tag(selector, parent)
        if node and attr in node.attrs:
            return node.get(attr)
        return default_value

    def try_get_list(self, selector: str, parent: Tag = None, default_value=None):
        text = self.try_get_text(selector, parent, default_value)
        if text:
            return [x.strip() for x in text.split(",")]
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

    def try_get_text(self, selector: str, parent: Tag = None, default_value=None):
        node = self.try_get_tag(selector, parent)
        if node:
            return node.text
        return default_value

    def get_next_sibling_of(self, selector: str, parent: Tag = None):
        node = self.try_get_tag(selector, parent)
        if node and node.next_sibling:
            return node.next_sibling
        return None

    def try_parse_mfc_time(self, date: str, default: datetime.datetime = None) -> datetime.datetime:
        try:
            # ex 12/21/2017, 13:01:50
            format = "%m/%d/%Y, %H:%M:%S"
            d = datetime.datetime.strptime(date, format)
            return d.replace(tzinfo=datetime.timezone.utc)
        except:
            return default

    def get_trailing_number(self, text: str) -> int:
        match = re.search(r"\d+$", text)
        if match:
            return int(match.group(0))
        return None

    def try_parse_pagination(self, parent: Tag = None) -> Pagination:
        p = parent if parent else self._soup
        pagination_controls = p.select_one("div.results-count")
        if pagination_controls is None:
            return None

        total_items = self.try_extract_number(
            pagination_controls.select_one("div.results-count-value").text
        )

        nav_controls = pagination_controls.select_one("div.results-count-pages")

        if nav_controls is None:
            return Pagination(
                current_page=1,
                has_next_page=False,
                total_pages=1,
                total_items=total_items,
            )

        current_link = nav_controls.select_one("a.nav-current")
        next_link = nav_controls.select_one("a.nav-next")
        last_link = nav_controls.select_one("a.nav-last.nav-end")

        current_page = self.try_extract_number(current_link.text)

        if last_link:
            total_pages = parse_qs(urlparse(last_link.get("href")).query)["page"][0]
        else:
            total_pages = current_page

        pagination = Pagination(
            current_page=current_page,
            has_next_page=next_link is not None,
            total_pages=total_pages,
            total_items=total_items,
        )

        return pagination
