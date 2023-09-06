from tenji.model.category import ItemCategory
from tenji.model.user.collection import Collection, CollectionStats
from tenji.model.item.item import Item
from tenji.parser.parser_base import ParserBase


class CollectionParser(ParserBase):
    def parse(self) -> Collection:
        items = []

        cat_links = self._soup.select_one("div.results-toggles").select("a")
        owned = self.try_extract_number(cat_links[0].text)
        ordered = self.try_extract_number(cat_links[1].text)
        wished = self.try_extract_number(cat_links[2].text)
        stats = CollectionStats(owned=owned, ordered=ordered, wished=wished)

        results = self._soup.select("div.results > div.result")

        # TODO check if collection is empty
        for result in results:
            stamp = result.select_one("div.stamp")
            link = stamp.select_one("a")
            id = self.try_extract_number(link.get("href"))
            thumbnail = link.select_one("img").get("src")
            name = link.select_one("img").get("alt")

            cat_node = result.select_one("div.stamp-category")
            cat_id = self.try_extract_number(cat_node.get("class")[-1])
            category = ItemCategory(cat_id)

            item = Item(
                id=id,
                name=name,
                thumbnail=thumbnail,
                category=category,
            )

            items.append(item)

        pagination = self.try_parse_pagination()
        return Collection(items=items, stats=stats, pagination=pagination)
