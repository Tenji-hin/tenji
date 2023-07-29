from unicodedata import category
from pydantic import BaseModel
from mfc.model.category import get_item_category_from_str
from mfc.model.collection import Collection
from mfc.model.item import Item
from mfc.model.paginated import Pagination
from mfc.parser import ParserBase


class CollectionParser(ParserBase):
    def parse(self) -> Collection:
        items = []

        results = self._soup.select("div.results > div.result")
        for result in results:
            stamp = result.select_one("div.stamp")
            link = stamp.select_one("a")
            id = self.try_extract_number(link.get("href"))
            thumbnail = link.select_one("img").get("src")
            name = link.select_one("img").get("alt")
            category = get_item_category_from_str(
                result.select_one("div.stamp-category").text
            )

            item = Item(
                id=id,
                name=name,
                thumbnail=thumbnail,
                category=category,
            )

            items.append(item)

        pagination_controls = self._soup.select_one("div.results-count-pages")

        if pagination_controls is None:
            return Collection(items=items)

        current_link = pagination_controls.select_one("a.nav-current")
        next_link = pagination_controls.select_one("a.nav-next")

        pagination = Pagination(
            current_page=self.try_extract_number(current_link.text),
            has_next_page=next_link is not None,
        )

        return Collection(items=items, pagination=pagination)
