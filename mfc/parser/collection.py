from mfc.model.collection import Collection
from mfc.model.item import Item
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

            item = Item(
                id=id,
                name=name,
                thumbnail=thumbnail,
            )

            items.append(item)

        return Collection(items=items)
