from mfc.model.category import get_item_category_from_str
from mfc.model.item.item import Item
from mfc.parser import ParserBase


class ItemParser(ParserBase):
    def parse(self) -> Item:
        id = self.try_extract_number(self._soup.select_one("a.current").text)
        name = self._soup.select_one("span.h1-headline-value > span").text
        thumbnail = self._soup.select_one("span.h1-headline-icon > img").get("src")
        category = get_item_category_from_str(
            self.get_next_sibling_of("span.icon-tag").text
        )

        return Item(id=id, name=name, thumbnail=thumbnail, category=category)