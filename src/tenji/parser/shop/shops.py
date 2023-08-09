from tenji.model.shop.shop_category import ShopCategory
from tenji.model.shop.shop_list_item import ShopListItem
from tenji.parser.parser_base import ParserBase


class ShopsParser(ParserBase):
    def parse(self) -> list[ShopListItem]:
        shops = []
        results = self._soup.select("#wide > div > section > div.results > div.result")

        for result in results:
            id = self.try_extract_number(result.select_one("a").attrs["href"])
            name = result.select_one("div.list-anchor a").text
            icon = result.select_one("img.list-icon").get("src")

            actions = result.select_one("div.list-actions")
            category = ShopCategory(
                self.try_extract_number(actions.select_one("a").attrs["href"][-3:])
            )
            location = self.try_get_text("a:nth-child(2)", actions)

            shops.append(
                ShopListItem(
                    id=id,
                    name=name,
                    icon=icon,
                    category=category,
                    location=location,
                )
            )

        return shops
